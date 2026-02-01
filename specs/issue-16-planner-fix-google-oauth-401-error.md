# Bug: Google OAuth 401 Unauthorized Error on Token Exchange

## Bug Description
After clicking "Sign in with Google" and completing the Google OAuth consent screen, the user is redirected back to the application with an error message: `OAuth error: Client error '401 Unauthorized' for url 'https://oauth2.googleapis.com/token'`. The user sees this error on the OAuth callback page and cannot complete the sign-in process.

**Symptoms:**
- User clicks "Sign in with Google" button
- User is redirected to Google and authenticates successfully
- Google redirects back to `/api/auth/google/callback` with an authorization code
- Backend attempts to exchange the code for tokens at `https://oauth2.googleapis.com/token`
- Google's token endpoint returns HTTP 401 Unauthorized
- User sees error message on `/oauth/callback` page

**Expected behavior:** User should be authenticated and redirected to the dashboard.

**Actual behavior:** User sees OAuth error message and cannot sign in.

## Problem Statement
The Google OAuth token exchange is failing with a 401 Unauthorized error. This occurs when the backend service attempts to exchange the authorization code for access tokens at Google's OAuth token endpoint. A 401 error from Google's token endpoint indicates one of:
1. Invalid or missing `client_id`
2. Invalid or missing `client_secret`
3. Mismatched `redirect_uri` (must exactly match what's registered in Google Cloud Console)
4. The authorization code has already been used or expired
5. OAuth credentials are not properly configured in the environment

The current implementation in `oauth_service.py` does not validate OAuth credentials before attempting the token exchange and does not provide helpful error messages to diagnose configuration issues.

## Solution Statement
Improve the Google OAuth implementation with the following fixes:

1. **Add early validation of OAuth credentials** - Check that `GOOGLE_CLIENT_ID` and `GOOGLE_CLIENT_SECRET` are configured before initiating the OAuth flow, providing clear error messages if they're missing.

2. **Improve error handling in token exchange** - Catch and parse the specific error from Google's response to provide actionable error messages (e.g., "invalid_client", "invalid_grant", "redirect_uri_mismatch").

3. **Add validation at OAuth URL generation** - Prevent users from starting the OAuth flow if credentials are not properly configured.

4. **Improve user-facing error messages** - Display more helpful error messages on the frontend callback page to help users and administrators diagnose the issue.

## Steps to Reproduce
1. Start the application with Docker Compose: `docker compose up -d`
2. Navigate to http://localhost:5173/login
3. Click "Sign in with Google" button
4. Complete Google authentication on the consent screen
5. Observe error on redirect: `OAuth error: Client error '401 Unauthorized' for url 'https://oauth2.googleapis.com/token'`

## Root Cause Analysis
The 401 Unauthorized error from Google's token endpoint (`https://oauth2.googleapis.com/token`) occurs during the OAuth 2.0 authorization code exchange. This is the second step in the OAuth flow where the application exchanges the authorization code (received from Google after user consent) for access and refresh tokens.

**Technical flow:**
1. User clicks "Sign in with Google"
2. Frontend calls `GET /api/auth/google` to get authorization URL
3. User is redirected to Google's consent screen
4. User approves, Google redirects to `GOOGLE_REDIRECT_URI` with `?code=AUTH_CODE`
5. Backend receives callback at `GET /api/auth/google/callback`
6. Backend calls `oauth_service.exchange_code_for_token(code)` (line 189 in `auth_service.py`)
7. `oauth_service` makes POST request to `https://oauth2.googleapis.com/token` (line 79-81 in `oauth_service.py`)
8. **Google returns 401 Unauthorized**

**Root causes (in order of likelihood):**

1. **Missing or invalid OAuth credentials** - The environment variables `GOOGLE_CLIENT_ID` and/or `GOOGLE_CLIENT_SECRET` are either:
   - Not set in `.env` file (empty strings by default in `config.py`)
   - Set to placeholder values instead of real credentials
   - Invalid/expired credentials from Google Cloud Console

2. **Redirect URI mismatch** - The `GOOGLE_REDIRECT_URI` in `.env` does not exactly match the authorized redirect URI configured in Google Cloud Console. Common issues:
   - HTTP vs HTTPS mismatch
   - Trailing slash difference
   - Port number mismatch
   - Different hostname (localhost vs 127.0.0.1)

3. **Authorization code reuse** - The authorization code can only be used once. If there's a retry mechanism or the callback is called twice, the second attempt will fail with 401.

**Code locations:**
- `app/server/services/oauth_service.py:51-82` - `exchange_code_for_token()` method that makes the failing request
- `app/server/services/oauth_service.py:65-69` - Existing validation only checks if credentials are set, but doesn't validate them
- `app/server/services/auth_service.py:188-189` - Where the token exchange is called
- `app/server/routers/auth.py:278-289` - Error handling that produces the user-facing error message

## Relevant Files
Use these files to fix the bug:

### Backend Files
- `app/server/services/oauth_service.py` - OAuth service that handles Google token exchange. Contains the `exchange_code_for_token()` method that needs improved error handling and credential validation.
- `app/server/services/auth_service.py` - Auth service that calls OAuth service. The `login_with_google()` method at line 170-264 handles the OAuth flow.
- `app/server/routers/auth.py` - Auth router with Google OAuth endpoints. The `/google` endpoint (line 206-220) and `/google/callback` endpoint (line 223-289) need validation improvements.
- `app/server/config.py` - Configuration settings including Google OAuth credentials. Defines `google_client_id`, `google_client_secret`, and `google_redirect_uri`.
- `app/server/.env.sample` - Environment variable template. Already has correct documentation for Google OAuth setup.

### Frontend Files
- `app/client/src/views/OAuthCallbackView.vue` - OAuth callback page that displays errors. Needs improved error message display.
- `app/client/src/composables/useGoogleAuth.js` - Google auth composable. Should handle configuration errors gracefully.
- `app/client/src/components/GoogleLoginButton.vue` - Google sign-in button component.

### Documentation
- `README.md` - Contains Google OAuth setup instructions.
- `resource/feature-user-auth-session-mgmt.md` - Auth feature documentation with OAuth troubleshooting section.
- `.claude/commands/test_e2e.md` - E2E test runner instructions.
- `.claude/commands/e2e/test_basic_query.md` - Example E2E test format.

### New Files
- `.claude/commands/e2e/test_google_oauth_error_handling.md` - New E2E test file to validate OAuth error handling.

## Step by Step Tasks
IMPORTANT: Execute every step in order, top to bottom.

### Step 1: Add Credential Validation to OAuth Service
- Edit `app/server/services/oauth_service.py`
- Add a new method `validate_credentials()` that checks if `client_id` and `client_secret` are set and non-empty
- Add a new method `is_configured()` that returns a boolean indicating if OAuth is properly configured
- Update `get_google_authorization_url()` to raise a clear `ValueError` if credentials are not configured, with a message like "Google OAuth is not configured. Please set GOOGLE_CLIENT_ID and GOOGLE_CLIENT_SECRET in your environment."

### Step 2: Improve Error Handling in Token Exchange
- Edit `app/server/services/oauth_service.py`
- Modify `exchange_code_for_token()` to catch `httpx.HTTPStatusError` separately
- Parse the error response body from Google to extract the specific error type (e.g., "invalid_client", "invalid_grant", "redirect_uri_mismatch")
- Map Google error types to user-friendly error messages:
  - `invalid_client`: "Invalid Google OAuth credentials. Please verify GOOGLE_CLIENT_ID and GOOGLE_CLIENT_SECRET."
  - `invalid_grant`: "Authorization code expired or already used. Please try signing in again."
  - `redirect_uri_mismatch`: "OAuth redirect URI mismatch. Please verify GOOGLE_REDIRECT_URI matches Google Cloud Console configuration."
- Re-raise as `ValueError` with the descriptive message

### Step 3: Add Validation to Auth Router Google Endpoint
- Edit `app/server/routers/auth.py`
- Update the `/google` endpoint (line 206-220) to check if OAuth is configured before returning the authorization URL
- If not configured, return HTTP 503 Service Unavailable with message "Google Sign-In is not available. OAuth credentials not configured."
- This prevents users from starting an OAuth flow that will inevitably fail

### Step 4: Improve Error Messages in Auth Router Callback
- Edit `app/server/routers/auth.py`
- Update the `/google/callback` endpoint exception handling (lines 278-289)
- For `ValueError` exceptions, pass the actual error message to the frontend
- For unexpected `Exception`, log the full error but return a generic user-friendly message
- Ensure sensitive information (client_secret) is never exposed in error messages

### Step 5: Improve Frontend Error Display
- Edit `app/client/src/views/OAuthCallbackView.vue`
- Update error display to show more helpful messages
- Add different error message styling/handling for configuration errors vs user errors
- Add a suggestion to contact administrator for configuration errors

### Step 6: Add Backend Unit Tests for OAuth Error Handling
- Edit or create `app/server/tests/test_oauth_service.py`
- Add test for `is_configured()` method
- Add test for `validate_credentials()` method
- Add test for proper error parsing in `exchange_code_for_token()` when Google returns errors
- Add test for `/api/auth/google` endpoint when OAuth is not configured

### Step 7: Create E2E Test for OAuth Error Handling
- Read `.claude/commands/e2e/test_basic_query.md` and `.claude/commands/e2e/test_google_oauth.md` to understand E2E test format
- Create new file `.claude/commands/e2e/test_google_oauth_error_handling.md`
- Include test steps:
  1. Navigate to login page
  2. Verify "Sign in with Google" button is present
  3. Click the button
  4. If OAuth not configured, verify appropriate error message is displayed
  5. Verify user can return to login page
  6. Take screenshots of error states
- Define success criteria for error handling scenarios

### Step 8: Run Validation Commands
Execute the validation commands to ensure the bug is fixed with zero regressions.

## Validation Commands
Execute every command to validate the bug is fixed with zero regressions.

### Pre-fix verification (document current behavior)
```bash
# Start the application
docker compose up -d

# Check if OAuth credentials are configured
grep -E "GOOGLE_CLIENT_(ID|SECRET)" app/server/.env 2>/dev/null || echo "OAuth credentials not found in .env"

# Test the /api/auth/google endpoint
curl -s http://localhost:8000/api/auth/google | jq .
```

### Post-fix verification
```bash
# Test OAuth endpoint when credentials are missing - should return 503
curl -s -w "\nHTTP Status: %{http_code}\n" http://localhost:8000/api/auth/google

# Test OAuth endpoint when credentials are configured - should return authorization URL
# (Requires valid credentials in .env)
curl -s http://localhost:8000/api/auth/google | jq .authorization_url
```

### Unit Tests
```bash
cd app/server && uv run pytest tests/test_oauth_service.py -v
```

### Full Test Suite
```bash
cd app/server && uv run pytest -v
```

### Frontend Type Checking
```bash
cd app/client && bun tsc --noEmit
```

### Frontend Build
```bash
cd app/client && bun run build
```

### E2E Test
Read `.claude/commands/test_e2e.md`, then read and execute `.claude/commands/e2e/test_google_oauth_error_handling.md` to validate OAuth error handling works correctly.

## Notes

### Configuration Requirements
To fully test Google OAuth after the fix:
1. Create a Google Cloud project at https://console.cloud.google.com/
2. Enable Google+ API
3. Create OAuth 2.0 Client ID (Web application)
4. Add authorized redirect URI: `http://localhost:8000/api/auth/google/callback`
5. Copy Client ID and Secret to `app/server/.env`:
   ```
   GOOGLE_CLIENT_ID=your-client-id.apps.googleusercontent.com
   GOOGLE_CLIENT_SECRET=your-client-secret
   GOOGLE_REDIRECT_URI=http://localhost:8000/api/auth/google/callback
   ```

### Common Google OAuth Error Codes
- `invalid_client` - Client ID or secret is wrong
- `invalid_grant` - Auth code expired (10 min) or already used
- `redirect_uri_mismatch` - Redirect URI doesn't match Console config
- `unauthorized_client` - App not authorized for this grant type
- `access_denied` - User denied consent

### Testing Without Valid Credentials
The fix should:
1. Prevent the OAuth flow from starting if credentials are not configured
2. Display a clear message that OAuth is not available
3. Allow the application to function normally for email/password authentication

### No New Dependencies Required
This fix uses existing libraries (httpx, FastAPI) - no new dependencies needed.

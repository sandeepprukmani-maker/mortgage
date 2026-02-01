# Plan: UWM API Connection Test Modal Under Settings Menu

## Description
Create a UWM API connection test page under the Settings menu that allows users to verify the UWM OAuth connection is working properly. The page should display an inline modal-style card centered on the page with:

1. **Card Layout**: Centered card on the settings page with:
   - Top-left: "UWM" text label in bold
   - Top-right: "Test Connection" button
   - Content area: Log output display (scrollable)

2. **Test Connection Functionality**: When user clicks "Test Connection":
   - Make a real API test connection using credentials configured in `.env`
   - Display real-time logs in the content area showing connection status

3. **Log Output Format**: Display logs similar to the sample output:
   ```
   INFO:services.uwm_auth_service:Outgoing IP address: 4.227.184.143
   INFO:services.uwm_auth_service:Sending OAuth request to: https://sso.uwm.com/adfs/oauth2/token
   INFO:services.uwm_auth_service:Using client_id: https://a69ec20e-77c5-4788-9965-691b65df9739/
   INFO:services.uwm_auth_service:Request body params: {
     'grant_type': 'client_credentials',
     'client_id': 'https://a69ec20e-77c5-4788-9965-691b65df9739/',
     'client_secret': '***',
     'scope': 'https://api.uwm.com/loanorigination-int',
     'username': None,
     'password': None
   }
   ERROR:services.uwm_auth_service:UWM OAuth error: invalid_client - MSIS9607: The 'client_id' parameter in the request is invalid.

   Summary:
   | Item        | Value                                              |
   |-------------|----------------------------------------------------|
   | Outgoing IP | 4.227.184.143 ✅ (correct staging IP)              |
   | client_id   | https://a69ec20e-77c5-4788-9965-691b65df9739/      |
   | scope       | https://api.uwm.com/loanorigination-int            |
   | Error       | invalid_client - client_id not registered with UWM |
   ```

4. **Connection Status Indicator**:
   - Show ✅ (checkmark) if connection succeeds
   - Show ❌ (cross) with error message if connection fails

5. **Navigation**: The page must be accessible from the existing "Settings" menu item in the sidebar (currently points to `/coming-soon`)

## Relevant Files
Use these files to resolve the chore:

### Backend Files
- `app/server/services/uwm_auth_service.py` - Contains the existing UWM OAuth authentication service with `_acquire_token()`, `_log_outgoing_ip()`, and token management methods. This will be used by the new test connection endpoint.
- `app/server/config.py` - Contains UWM configuration settings (`uwm_sso_url`, `uwm_client_id`, `uwm_client_secret`, `uwm_scope`, `uwm_environment`, etc.)
- `app/server/routers/pricing.py` - Existing pricing router, will serve as reference for creating the new test connection endpoint
- `app/server/main.py` - Main FastAPI application where the new router will be registered
- `app/server/routers/__init__.py` - Router exports file

### Frontend Files
- `app/client/src/components/PricingModal.vue` - Existing modal component that can be used as a reference for card styling (uses Transition, backdrop, header/body/footer structure)
- `app/client/src/components/ui/BaseButton.vue` - Reusable button component
- `app/client/src/components/ui/BaseCard.vue` - Reusable card component for the settings card
- `app/client/src/components/sidebar/AppSidebar.vue` - Sidebar component with existing "Settings" menu item at line 90 that links to `/coming-soon` - needs to be updated to `/settings`
- `app/client/src/router/index.js` - Router configuration - needs new `/settings` route added
- `app/client/src/views/ComingSoonView.vue` - Reference for view structure

### New Files
- `app/server/routers/uwm.py` - New router with test connection endpoint
- `app/server/schemas/uwm.py` - Pydantic schemas for UWM test connection request/response
- `app/client/src/views/SettingsView.vue` - New settings view to house the UWM connection test card
- `app/client/src/services/uwmService.js` - Frontend service for calling the test connection API

## Step by Step Tasks
IMPORTANT: Execute every step in order, top to bottom.

### Step 1: Create Backend Schema for UWM Test Connection

- Create `app/server/schemas/uwm.py` with Pydantic schemas:
  - `UWMTestConnectionResponse` schema with fields:
    - `success: bool` - Whether connection succeeded
    - `outgoing_ip: str | None` - The detected outgoing IP address
    - `sso_url: str` - The UWM SSO URL being used
    - `client_id: str` - The client ID being used (for display)
    - `scope: str` - The OAuth scope being used
    - `grant_type: str` - The grant type (password or client_credentials)
    - `error: str | None` - Error message if connection failed
    - `logs: list[str]` - List of log messages from the connection attempt

### Step 2: Add Test Connection Method to UWM Auth Service

- Modify `app/server/services/uwm_auth_service.py`:
  - Add a new method `async def test_connection(self) -> dict` that:
    - Collects logs during the connection attempt using a custom log handler
    - Calls `_log_outgoing_ip()` to get the IP
    - Attempts to acquire a token using `_acquire_token()`
    - Returns a dictionary with connection status, IP, credentials info, and collected logs
    - Catches exceptions and returns error information
  - Create a `ListHandler` class that extends `logging.Handler` to capture logs to a list

### Step 3: Create UWM Router with Test Connection Endpoint

- Create `app/server/routers/uwm.py`:
  - Create `POST /api/uwm/test-connection` endpoint
  - Import `UWMAuthService` and `UWMTestConnectionResponse`
  - Endpoint should:
    - Instantiate a fresh UWMAuthService (not the singleton) for isolated testing
    - Call the test connection method on the UWM auth service
    - Return structured response with logs and status
  - Protect endpoint with authentication using `get_current_user` dependency

### Step 4: Register UWM Router in Main Application

- Modify `app/server/main.py`:
  - Import the new `uwm` router from `routers`
  - Add the router with prefix `/api/uwm` and tag "UWM"

### Step 5: Update Router Exports

- Modify `app/server/routers/__init__.py`:
  - Import and export the new `uwm` router

### Step 6: Create Frontend UWM Service

- Create `app/client/src/services/uwmService.js`:
  - Import `apiClient` from existing API setup (check how other services import it, e.g., `customerService.js`)
  - Create `testConnection()` async function that calls `POST /api/uwm/test-connection`
  - Return the response data

### Step 7: Create Settings View with UWM Connection Test Card

- Create `app/client/src/views/SettingsView.vue`:
  - Use standard view layout with page title "Settings"
  - Create a "UWM Integration" section
  - Add an inline card (not a popup modal) that is centered on the page with:
    - **Header Row**:
      - Left side: "UWM" text in bold (text-xl font-bold)
      - Right side: "Test Connection" button using `BaseButton` component
    - **Body Area**:
      - Log display area with monospace font (`font-mono`)
      - Pre-formatted text showing connection logs (`<pre>` tag)
      - Scrollable area with max-height (`max-h-96 overflow-y-auto`)
      - Initially show placeholder text like "Click 'Test Connection' to verify UWM API connectivity"
    - **Footer/Summary Area**:
      - Connection status summary table showing:
        - Outgoing IP (with ✅ or ❌)
        - Client ID (masked partially for security)
        - Scope
        - Status (Success ✅ or Error ❌ with message)
      - Only show summary after test is run
  - **Component State**:
    - `loading: ref(false)` - Loading state for button spinner
    - `logs: ref([])` - Array of log strings
    - `connectionResult: ref(null)` - Full response object
    - `hasRun: ref(false)` - Whether test has been run at least once
  - **Methods**:
    - `testConnection()` - Calls the API and updates state
    - Clear previous logs when starting new test
    - Show loading spinner on button while testing

### Step 8: Add Settings Route to Router

- Modify `app/client/src/router/index.js`:
  - Add new route object:
    ```javascript
    {
      path: '/settings',
      name: 'Settings',
      component: () => import('../views/SettingsView.vue'),
      meta: { requiresAuth: true },
    },
    ```
  - Place it near other authenticated routes

### Step 9: Update Sidebar Navigation to Point to Settings

- Modify `app/client/src/components/sidebar/AppSidebar.vue`:
  - Change line 90 from `to="/coming-soon"` to `to="/settings"` for the Settings menu item

### Step 10: Style the Card for Centered Display

- In `SettingsView.vue`, ensure the card:
  - Uses appropriate container width (e.g., `max-w-3xl mx-auto`)
  - Has proper padding and shadow (`shadow-lg rounded-lg`)
  - Uses white background with border (`bg-white border border-gray-200`)
  - Has proper section spacing

### Step 11: Run Validation Commands

- Run all validation commands to ensure the chore is complete with zero regressions

## Validation Commands
Execute every command to validate the chore is complete with zero regressions.

- `cd app/server && uv run pytest` - Run server tests to validate the chore is complete with zero regressions
- `cd app/client && npx vue-tsc --noEmit` - Run TypeScript type checking for the client
- `cd app/client && bun run build` - Build the frontend to ensure no compilation errors

## Notes

### UWM Auth Service Integration
The existing `uwm_auth_service.py` already has all the necessary methods for OAuth token acquisition:
- `_log_outgoing_ip()` - Fetches outgoing IP via api.ipify.org
- `_acquire_token()` - Performs OAuth token acquisition with full logging
- `_parse_uwm_error()` - Parses UWM SSO error responses

The test connection endpoint should leverage these existing methods rather than duplicating code.

### Log Capture Strategy
To capture logs during the test connection:
```python
import logging

class ListHandler(logging.Handler):
    def __init__(self):
        super().__init__()
        self.logs = []

    def emit(self, record):
        self.logs.append(self.format(record))

# Usage in test_connection method:
handler = ListHandler()
handler.setFormatter(logging.Formatter('%(levelname)s:%(name)s:%(message)s'))
logger.addHandler(handler)
try:
    # ... perform test
finally:
    logger.removeHandler(handler)
return {"logs": handler.logs, ...}
```

### Security Considerations
- The test connection endpoint should be protected with authentication
- Consider restricting to admin users only in the future
- Sensitive data (client_secret, password) should be masked in logs (already done in existing code)

### Environment Variables Used
The connection test uses these env vars from `config.py`:
- `UWM_SSO_URL` - OAuth endpoint (default: `https://sso.uwm.com/adfs/oauth2/token`)
- `UWM_CLIENT_ID` - OAuth client ID
- `UWM_CLIENT_SECRET` - OAuth client secret
- `UWM_SCOPE` - OAuth scope (or derived from `UWM_ENVIRONMENT`)
- `UWM_USERNAME` / `UWM_PASSWORD` - For password grant type (optional)
- `UWM_ENVIRONMENT` - dev/staging/production (determines scope if not explicitly set)

### Existing Sidebar Structure
The sidebar already has a "Settings" group with a "Settings" item (line 81-98 in AppSidebar.vue):
```vue
<SidebarMenuGroup title="Settings">
  <SidebarMenuItem to="/profile" label="Profile">...</SidebarMenuItem>
  <SidebarMenuItem to="/coming-soon" label="Settings">...</SidebarMenuItem>
</SidebarMenuGroup>
```
The Settings link currently goes to `/coming-soon` and needs to be updated to `/settings`.

### Card vs Modal Decision
Per the requirements, this should be an "inline modal" style - which means a card component embedded in the page (not a popup overlay modal). The card should be centered on the settings page and styled to look like a modal (shadow, rounded corners, white background) but remain inline with the page content.

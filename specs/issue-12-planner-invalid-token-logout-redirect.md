# Plan: Invalid Access Token Auto-Logout and Redirect to Login

## Description
When a user has an invalid or expired access token and the token refresh also fails, the application should properly logout the user and redirect them to the login page. Currently, the implementation only removes the token from localStorage but doesn't properly clear the Pinia auth store state, which can leave the application in an inconsistent state.

The fix should:
1. Properly clear the auth store state using `clearAuth()` when token refresh fails
2. Use Vue Router for navigation instead of `window.location.href` for a smoother SPA experience
3. Ensure the user store is also cleared if it contains user data

## Relevant Files
Use these files to resolve the chore:

- `app/client/src/services/api.js` - The main API client with axios interceptors that handle 401 errors and token refresh. This is where the logout/redirect logic needs to be improved (lines 110-114).
- `app/client/src/stores/auth.js` - The Pinia auth store with `clearAuth()` method that properly clears authentication state and localStorage.
- `app/client/src/stores/user.js` - The Pinia user store that may need to be cleared on logout.
- `app/client/src/router/index.js` - Vue Router instance for programmatic navigation.
- `resource/feature-user-auth-session-mgmt.md` - Documentation for the authentication system.

## Step by Step Tasks
IMPORTANT: Execute every step in order, top to bottom.

### Step 1: Update API Service to Properly Handle Token Refresh Failure

- Modify `app/client/src/services/api.js`:
  - Import the auth store: `import { useAuthStore } from '../stores/auth';`
  - Import the user store: `import { useUserStore } from '../stores/user';`
  - Import the router: `import router from '../router';`
  - In the catch block for refresh token failure (around line 110-114), update to:
    ```javascript
    } catch (refreshError) {
      processQueue(refreshError, null);

      // Properly clear auth state using store methods
      const authStore = useAuthStore();
      const userStore = useUserStore();
      authStore.clearAuth();
      userStore.clearUser();

      // Use router for navigation instead of window.location
      router.push({ name: 'Login' });

      return Promise.reject(refreshError);
    }
    ```

### Step 2: Verify User Store Has clearUser Method

- Check `app/client/src/stores/user.js` for a `clearUser()` method
- If it doesn't exist, add it:
  ```javascript
  function clearUser() {
    user.value = null;
  }
  ```
- Export the method in the store's return statement

### Step 3: Handle Edge Case - 401 on Initial Page Load

- The current implementation may have issues if a 401 occurs before the app is fully initialized
- Ensure the stores can be safely accessed even if Pinia hasn't fully initialized
- Consider adding a try-catch around store usage to fall back to localStorage removal if stores aren't available

### Step 4: Run Validation Commands

- Run all validation commands to ensure the chore is complete with zero regressions

## Validation Commands
Execute every command to validate the chore is complete with zero regressions.

- `cd app/client && npm run build` - Build the frontend to ensure no compilation errors
- `cd app/server && uv run pytest` - Run server tests to validate no regressions

## Notes

### Current Behavior
The current implementation in `api.js` lines 110-114:
```javascript
} catch (refreshError) {
  processQueue(refreshError, null);
  localStorage.removeItem('accessToken');
  window.location.href = '/login';
  return Promise.reject(refreshError);
}
```

This has issues:
1. Only clears localStorage, not the Pinia store reactive state
2. `authStore.isAuthenticated` remains true until page reload because it's based on the reactive `accessToken` ref
3. `window.location.href` causes a full page reload instead of SPA navigation

### Expected Behavior
When token refresh fails:
1. Clear auth store state (which also clears localStorage)
2. Clear user store state
3. Navigate to login page using Vue Router
4. User sees login page immediately without a full page reload

### Testing Scenarios
To test this fix:
1. Login to the application
2. Manually delete the refresh token cookie from browser DevTools
3. Make any API request or wait for access token to expire
4. The app should redirect to login page without issues
5. The auth store should show `isAuthenticated: false`

### Potential Edge Case
If Pinia stores haven't initialized yet (rare edge case on initial page load), the code should gracefully fall back to the current behavior of just clearing localStorage and redirecting.

# Plan: Fix User Avatar Showing "US" Instead of Actual User Initials

## Description
The user avatar in the header sometimes shows "US" with a blue background instead of the actual logged-in user's initials, name, and email. This happens because:

1. On page refresh or initial load, the app only checks for an access token in localStorage (`authStore.checkAuth()`)
2. The user profile is **not** being fetched from the API after authentication is confirmed
3. The `HeaderUserMenu.vue` component then shows default values:
   - Avatar initials: "US" (derived from "User" - the fallback name when no profile exists)
   - Name: "User"
   - Email: empty

The fix requires fetching the user profile in `App.vue` when the user is authenticated on initial page load.

## Relevant Files
Use these files to resolve the chore:

- `app/client/src/App.vue` - Main app component where `authStore.checkAuth()` is called on mount. This is where we need to add the profile fetch logic.
- `app/client/src/stores/user.js` - User store with `fetchProfile()` method that needs to be called.
- `app/client/src/stores/auth.js` - Auth store with `checkAuth()` method and `isAuthenticated` computed property.
- `app/client/src/components/header/HeaderUserMenu.vue` - The component displaying the user avatar, name, and email (for reference only, no changes needed here).
- `app/client/src/composables/useAuth.js` - Shows the login flow calls `fetchProfile()` after login (for reference).

## Step by Step Tasks
IMPORTANT: Execute every step in order, top to bottom.

### Step 1: Update App.vue to Fetch User Profile on Initial Load

- Modify `app/client/src/App.vue`:
  - Import the user store: `import { useUserStore } from './stores/user';`
  - Initialize the user store: `const userStore = useUserStore();`
  - Update the `onMounted` hook to fetch the user profile if authenticated:
    ```javascript
    onMounted(async () => {
      themeStore.initTheme();
      const hasAuth = authStore.checkAuth();

      // Fetch user profile if authenticated
      if (hasAuth) {
        try {
          await userStore.fetchProfile();
        } catch (error) {
          // If profile fetch fails (e.g., token expired), auth will handle redirect
          console.error('Failed to fetch user profile:', error);
        }
      }
    });
    ```

### Step 2: Run Validation Commands

- Run all validation commands to ensure the chore is complete with zero regressions

## Validation Commands
Execute every command to validate the chore is complete with zero regressions.

- `cd app/client && npm run build` - Build the frontend to ensure no compilation errors
- `cd app/server && uv run pytest` - Run server tests to validate no regressions

## Notes

### Root Cause Analysis
The issue occurs because:
1. `authStore.checkAuth()` only verifies a token exists in localStorage and sets `isAuthenticated` to true
2. `userStore.profile` remains `null` since no API call is made to fetch the profile
3. `HeaderUserMenu.vue` falls back to showing "User" when no profile exists:
   ```javascript
   const userName = computed(() => {
     if (userProfile.value?.first_name || userProfile.value?.last_name) {
       return `${userProfile.value?.first_name || ''} ${userProfile.value?.last_name || ''}`.trim();
     }
     return userProfile.value?.email?.split('@')[0] || 'User';  // Falls back to 'User'
   });

   const userInitials = computed(() => {
     const name = userName.value;  // 'User'
     const parts = name.split(' ');  // ['User']
     if (parts.length >= 2) { ... }
     return name.substring(0, 2).toUpperCase();  // 'US'
   });
   ```

### Why Login Works But Page Refresh Doesn't
- When logging in via `useAuth.login()`, it explicitly calls `await userStore.fetchProfile()` after setting auth
- On page refresh, only `checkAuth()` is called which doesn't fetch the profile

### Alternative Approaches Considered
1. **Fetch profile in router guard** - More complex, would need to handle async navigation
2. **Fetch profile in DashboardLayout** - Would cause multiple fetches if user navigates between pages
3. **Store profile in localStorage** - Would require syncing with server data, cache invalidation issues
4. **Fetch profile in App.vue on mount** - Simple, runs once, correct solution

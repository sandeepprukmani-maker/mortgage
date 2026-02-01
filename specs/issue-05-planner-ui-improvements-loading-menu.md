# Feature: UI Improvements - Loading Indicators, Menu Layout, and Dashboard Cleanup

## Feature Description
This feature implements several UI/UX improvements to enhance the user experience across the Valargen application. The improvements include:

1. **Global Loading Indicator**: Add visual feedback for all API calls to inform users when data is being fetched or actions are being processed
2. **Menu Layout Reorganization**: Restructure the top navigation menu to improve visual hierarchy by moving navigation items to the left while keeping user-specific actions (Profile and Logout) on the right
3. **Active Menu Item Highlighting**: Provide visual feedback to indicate which page the user is currently viewing
4. **Dashboard Simplification**: Streamline the dashboard view by removing complex content cards and focusing on a clean welcome message

These changes will improve usability, provide better visual feedback, and create a cleaner, more intuitive interface for users managing their mortgage workflows.

## User Story
As a Valargen user
I want clear visual feedback about system state and my current location in the application
So that I understand when the system is processing, know where I am in the navigation, and have a cleaner, more focused dashboard experience

## Problem Statement
Currently, the Valargen application lacks consistent visual feedback during API operations, making it unclear when the system is processing requests. The top navigation menu places all items together without clear visual hierarchy, and users cannot easily identify which page they're currently viewing. Additionally, the dashboard displays multiple content cards that may overwhelm users when they first log in.

## Solution Statement
We will implement a global loading indicator system that displays during all API calls, reorganize the navigation menu to separate navigation items from user actions, add active state highlighting to menu items, and simplify the dashboard to show only essential welcome information. This will be achieved by:

1. Adding a loading state management system using Pinia store
2. Integrating loading indicators into the API interceptor in `app/client/src/services/api.js`
3. Creating a global loading component that displays during API operations
4. Restructuring the `AppNavbar.vue` component to use flexbox layout with left-aligned navigation and right-aligned user actions
5. Implementing active route detection using Vue Router's built-in functionality
6. Simplifying `DashboardView.vue` to display only the welcome message

## Relevant Files
Use these files to implement the feature:

### Client Files (UI Components & State Management)
- **app/client/src/components/AppNavbar.vue** - Navigation component that needs layout restructuring and active state highlighting. Currently has all menu items in a single flex group on the right side.
- **app/client/src/views/DashboardView.vue** - Dashboard view that needs simplification. Currently displays role cards, organization info, and available modules sections.
- **app/client/src/services/api.js** - Axios instance with interceptors. This is where we'll integrate loading state management for all API calls.
- **app/client/src/App.vue** - Root component where the global loading indicator component will be added.
- **app/client/src/style.css** - Contains theme variables and styling that can be used for loading indicator and active menu states.

### State Management
- **app/client/src/stores/loading.js** (NEW FILE) - New Pinia store to manage global loading state for API operations.

### Loading Component
- **app/client/src/components/ui/LoadingIndicator.vue** (NEW FILE) - New global loading indicator component that displays during API operations.

### Router
- **app/client/src/router/index.js** - Router configuration needed to understand current route for active menu highlighting.

### Testing & Documentation
- **README.md** - Project documentation that describes the application architecture and tech stack.
- **.claude/commands/conditional_docs.md** - Conditional documentation guide for determining what documentation to read.
- **.claude/commands/test_e2e.md** - E2E test runner instructions for creating and executing tests.
- **.claude/commands/e2e/test_user_login.md** - Example E2E test file showing the structure and format.

### New Files

#### State Management
- **app/client/src/stores/loading.js** - Pinia store for managing global loading state with actions to show/hide loading indicator.

#### UI Components
- **app/client/src/components/ui/LoadingIndicator.vue** - Global loading indicator component with spinner animation and overlay.

#### E2E Test
- **.claude/commands/e2e/test_ui_improvements.md** - E2E test file to validate loading indicators, menu layout, active highlighting, and simplified dashboard.

## Implementation Plan
### Phase 1: Foundation
Create the infrastructure for loading state management by implementing a Pinia store and integrating it with the existing API interceptor. This provides the foundation for showing loading indicators across the application.

### Phase 2: Core Implementation
Implement the loading indicator UI component and restructure the navigation menu layout. Add active menu item highlighting using Vue Router's built-in features. Simplify the dashboard view to display only the welcome message.

### Phase 3: Integration
Integrate all components together, ensure the loading indicator displays during API calls, verify menu layout and highlighting works correctly, and validate the simplified dashboard. Create comprehensive E2E tests to ensure all features work as expected.

## Step by Step Tasks
IMPORTANT: Execute every step in order, top to bottom.

### 1. Create Loading State Management Store
- Create `app/client/src/stores/loading.js` as a new Pinia store
- Add reactive state for `isLoading` (boolean) and `loadingCount` (number to track concurrent requests)
- Implement `startLoading()` action to increment counter and set isLoading to true
- Implement `stopLoading()` action to decrement counter and set isLoading to false when counter reaches 0
- Export the store using `defineStore` with id 'loading'

### 2. Create Global Loading Indicator Component
- Create `app/client/src/components/ui/LoadingIndicator.vue`
- Import and use the loading store via `useLoadingStore()`
- Add a fixed overlay with semi-transparent background that covers the entire viewport
- Add a centered spinner animation using CSS or SVG
- Use `v-if="loadingStore.isLoading"` to conditionally render the loading indicator
- Style the spinner using the primary color from `style.css` theme variables
- Add smooth fade-in/fade-out transitions

### 3. Integrate Loading State with API Interceptor
- Open `app/client/src/services/api.js`
- Import the loading store at the top of the file
- In the request interceptor (before line 28), call `loadingStore.startLoading()`
- In the response interceptor success handler (after line 50), call `loadingStore.stopLoading()`
- In the response interceptor error handler (in the finally block around line 93), call `loadingStore.stopLoading()`
- Ensure loading state is properly decremented even when requests fail or are cancelled

### 4. Add Loading Indicator to App Root
- Open `app/client/src/App.vue`
- Import the `LoadingIndicator` component
- Add `<LoadingIndicator />` component to the template before `<router-view />`
- This ensures the loading indicator is available globally across all views

### 5. Restructure Navigation Menu Layout
- Open `app/client/src/components/AppNavbar.vue`
- Modify the main nav container to use `justify-between` instead of current layout
- Create a left-aligned div containing navigation items (Dashboard link)
- Create a right-aligned div containing Profile and Logout
- Keep the logo on the far left in its current position
- Update the flex container structure: logo (left) | nav items (center-left) | profile/logout (right)
- Ensure responsive design is maintained with existing Tailwind classes

### 6. Implement Active Menu Item Highlighting
- In `app/client/src/components/AppNavbar.vue`
- For each `router-link` (Dashboard and Profile), add dynamic class binding
- Use Vue Router's `$route.path` or `$route.name` to detect the current route
- Add conditional classes: when active, apply `text-primary-600 font-semibold border-b-2 border-primary-500` or similar styling
- When inactive, keep existing `text-gray-600` styling
- Use computed properties or inline conditions like `:class="{ 'text-primary-600 font-semibold': $route.name === 'Dashboard' }"`
- Test that active state updates when navigating between pages

### 7. Simplify Dashboard View
- Open `app/client/src/views/DashboardView.vue`
- Keep only the `AppNavbar` component and the welcome message header section
- Remove the following sections:
  - The grid container with role, organization, and subscription cards (lines 11-49)
  - The "Available Modules" section with all module cards (lines 52-98)
- Keep the welcome message: `<h2 class="m-0 text-3xl text-gray-800">Welcome, {{ userProfile?.first_name || 'User' }}!</h2>`
- Optionally keep the subtitle: `<p class="mt-2 text-gray-500 text-lg">Manage your mortgage automation workflows from here</p>`
- Center the welcome content on the page using flexbox or similar layout
- Maintain the background color and navbar integration

### 8. Create E2E Test for UI Improvements
- Create `.claude/commands/e2e/test_ui_improvements.md`
- Include User Story describing the UI improvements being tested
- Add test steps to validate:
  - Loading indicator appears during API calls (login, profile fetch)
  - Loading indicator disappears when API call completes
  - Navigation menu has proper layout (items on left, profile/logout on right)
  - Dashboard link is highlighted when on dashboard page
  - Profile link is highlighted when on profile page
  - Dashboard shows only welcome message (no cards or modules)
- Include screenshots for: menu layout, active highlighting on dashboard, active highlighting on profile, simplified dashboard, loading indicator during API call
- Follow the format from `.claude/commands/e2e/test_user_login.md`

### 9. Run Validation Commands
- Execute all validation commands listed below to ensure zero regressions
- Fix any issues that arise during validation
- Verify E2E tests pass successfully

## Testing Strategy
### Unit Tests
Since this feature primarily involves UI changes and state management:

1. **Loading Store Tests**: Test that `startLoading()` increments counter and sets isLoading to true, `stopLoading()` decrements counter and sets isLoading to false when counter reaches 0
2. **Component Tests**: Verify LoadingIndicator displays when isLoading is true and hides when false
3. **Navigation Tests**: Verify active class is applied to the correct menu item based on current route

### Edge Cases
1. **Concurrent API Calls**: Multiple simultaneous API requests should show loading indicator until ALL complete
2. **Failed API Calls**: Loading indicator should hide even when API calls fail
3. **Navigation During Loading**: User should be able to navigate while loading indicator is displayed
4. **No User Profile**: Dashboard welcome message should display "Welcome, User!" if first_name is null/undefined
5. **Long API Calls**: Loading indicator should remain visible for the entire duration of slow API calls
6. **Quick API Calls**: Loading indicator should handle rapid show/hide cycles gracefully

## Acceptance Criteria
- [ ] Loading indicator appears during all API calls (login, registration, profile fetch, logout, etc.)
- [ ] Loading indicator displays a spinner centered on screen with semi-transparent overlay
- [ ] Loading indicator handles concurrent requests correctly (doesn't hide until all complete)
- [ ] Navigation menu has Dashboard link on the left side of the navbar
- [ ] Navigation menu has Profile and Logout on the right side of the navbar
- [ ] Currently active menu item is visually highlighted with distinct color and styling
- [ ] Dashboard view displays only the welcome message with user's first name
- [ ] Dashboard view has no role cards, organization info, or available modules sections
- [ ] All existing functionality continues to work without regressions
- [ ] E2E test validates all four improvements work correctly
- [ ] Frontend build completes without errors
- [ ] Frontend type checking passes without errors
- [ ] All existing tests continue to pass

## Validation Commands
Execute every command to validate the feature works correctly with zero regressions.

- Read `.claude/commands/test_e2e.md`, then read and execute `.claude/commands/e2e/test_ui_improvements.md` to validate loading indicators, menu layout, active highlighting, and simplified dashboard
- `cd app/server && uv run pytest` - Run server tests to validate the feature works with zero regressions
- `cd app/client && bun tsc --noEmit` - Run frontend type checking to validate the feature works with zero regressions
- `cd app/client && bun run build` - Run frontend build to validate the feature works with zero regressions

## Notes
- The loading state management uses a counter pattern to handle concurrent API requests correctly
- The loading indicator should be lightweight and not block user input unnecessarily (users should still be able to navigate)
- Active menu highlighting should use the existing primary color from the theme (`--color-primary-500` or `--color-primary-600`)
- The dashboard simplification removes content but keeps the component structure intact for future additions
- Consider adding a minimum display time for the loading indicator (e.g., 200ms) to prevent flickering on very fast API calls
- The navbar layout change uses CSS flexbox with `justify-between` to separate navigation items from user actions
- Future enhancement: Add skeleton loaders for specific components instead of just a global spinner
- Future enhancement: Add loading states to individual buttons for better UX on form submissions

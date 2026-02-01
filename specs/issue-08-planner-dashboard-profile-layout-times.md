# Plan: Dashboard Left Side Right Side Profile Show All Times

## Description
This chore involves UI layout improvements and displaying all time-related fields in the Dashboard and Profile views:

1. **Dashboard Layout**: Adjust the dashboard view to have a left side and right side layout structure (two-column layout)
2. **Profile - Show All Times**: Display all time-related fields in the Profile view:
   - `created_at` - When the user account was created
   - `last_login_at` - When the user last logged in (already displayed)

Currently, the Profile view only shows `last_login_at`. This chore will add `created_at` to show the full account timeline.

## Relevant Files
Use these files to resolve the chore:

- `app/client/src/views/DashboardView.vue` - Main dashboard view that needs layout restructuring to have left side and right side columns
- `app/client/src/views/ProfileView.vue` - Profile page that contains the UserProfile component
- `app/client/src/components/UserProfile.vue` - Component that displays user profile details, needs to show `created_at` timestamp
- `app/client/src/stores/user.js` - User store that fetches profile data (already includes `created_at` from backend)
- `app/server/schemas/user.py` - Backend schema confirming `created_at` and `last_login_at` are available in UserResponse/UserProfile

## Step by Step Tasks
IMPORTANT: Execute every step in order, top to bottom.

### Step 1: Update Dashboard Layout to Two-Column (Left/Right) Structure
- Modify `app/client/src/views/DashboardView.vue` to restructure the layout:
  - Create a `.dashboard-layout` wrapper with CSS Grid or Flexbox for two columns
  - Left column (`.dashboard-left`): Contains the welcome header and info-cards section
  - Right column (`.dashboard-right`): Contains the modules-section
- Update the CSS to use a responsive two-column layout:
  - Desktop: Two columns (left ~40%, right ~60% or similar proportions)
  - Mobile: Stack vertically (single column)
- Ensure the existing content flows properly into the new layout structure

### Step 2: Update Profile View to Show All Time-Related Fields
- Modify `app/client/src/components/UserProfile.vue` to display the `created_at` timestamp:
  - Add a new detail row in the "Account Information" section for "Member Since" or "Account Created"
  - Use the existing `formatDate` function to format the `created_at` timestamp
  - Position it logically (e.g., before "Last Login" to show chronological order)
- Ensure the `created_at` field is displayed with the same formatting as `last_login_at`

### Step 3: Run Validation Commands
- Run the TypeScript/Vue type checking to ensure no type errors
- Run the server tests to ensure no regressions
- Verify the client builds successfully

## Validation Commands
Execute every command to validate the chore is complete with zero regressions.

- `cd app/client && npx vue-tsc --noEmit` - Run Vue TypeScript checking to validate no type errors
- `cd app/server && uv run pytest` - Run server tests to validate the chore is complete with zero regressions
- `cd app/client && npm run build` - Build the client to ensure no build errors

## Notes
- The backend already returns `created_at` in the UserProfile schema, so no backend changes are needed
- The `formatDate` function in `UserProfile.vue` can be reused for formatting `created_at`
- The two-column layout should be responsive and collapse to single column on mobile devices
- Use CSS Grid for the dashboard layout as it provides better control over column sizing

# Plan: Add Logo, Favicon, and Shared Navbar Component

## Description
Add the ValerGen logo to the application in three places:
1. **Favicon**: Create a favicon from the logo for browser tab identification
2. **Dashboard Navbar**: Replace the text "Valargen" with the logo image
3. **Profile Navbar**: Replace the text "Valargen" with the logo image

Additionally, the Dashboard and Profile views currently have duplicated navbar code. These should be refactored to use a single shared `AppNavbar` component to ensure consistency and maintainability.

The logo features:
- A blue square icon with a stylized "V" and orange wave accents
- "ValerGen" text in blue

## Relevant Files
Use these files to resolve the chore:

- **`app/client/index.html`** - Add favicon link tag to the HTML head section
- **`app/client/src/views/DashboardView.vue`** - Contains duplicated navbar code (lines 3-21) that needs to be replaced with the shared component
- **`app/client/src/views/ProfileView.vue`** - Contains duplicated navbar code (lines 3-11) that needs to be replaced with the shared component
- **`app/client/src/style.css`** - Global styles reference (may need updates for navbar consistency)

### New Files
- **`app/client/public/`** - Directory to create for static assets (favicon, logo images)
- **`app/client/public/favicon.ico`** - Favicon file to be created from the logo
- **`app/client/public/logo.svg`** - Full logo (icon + text) for navbar branding
- **`app/client/public/logo-icon.svg`** - Icon-only version for favicon source
- **`app/client/src/components/AppNavbar.vue`** - New shared navbar component

## Step by Step Tasks
IMPORTANT: Execute every step in order, top to bottom.

### Step 1: Create Public Directory and Add Logo Assets
- Create the `app/client/public/` directory if it doesn't exist
- Save the provided logo image as SVG files:
  - `logo.svg` - Full logo with icon and "ValerGen" text for navbar display
  - `logo-icon.svg` - Icon-only version (the blue square with V and orange waves) for favicon
- The logo SVG should be recreated based on the provided image:
  - Blue square border with rounded corners (#3D3DBF approximate color)
  - Stylized "V" inside the square in the same blue
  - Three orange curved wave strokes (#FF8C00 approximate color) emerging from bottom-left
  - "ValerGen" text to the right in blue (#3D3DBF)

### Step 2: Create Favicon
- Convert the logo icon to favicon format:
  - Create `favicon.ico` file (or use `favicon.svg` for modern browsers)
  - Recommended sizes: 16x16, 32x32, and 48x48 pixels
  - Use the icon portion only (blue square with V and orange waves)
- Update `app/client/index.html` to include the favicon:
  ```html
  <link rel="icon" type="image/x-icon" href="/favicon.ico" />
  ```
  Or for SVG favicon:
  ```html
  <link rel="icon" type="image/svg+xml" href="/favicon.svg" />
  ```

### Step 3: Create Shared AppNavbar Component
- Create `app/client/src/components/AppNavbar.vue` with the following features:
  - Display the logo image instead of text "Valargen"
  - Logo should link to home/dashboard (`/` or `/dashboard`)
  - Accept props for:
    - `showProfileLink` (boolean) - whether to show Profile link
    - `showDashboardLink` (boolean) - whether to show Dashboard link
  - Include the logout button functionality
  - Emit a `logout` event or use the auth composable directly
  - Maintain the existing styling (white background, shadow, flex layout)
  - Logo image should be appropriately sized (height ~32-40px recommended)

### Step 4: Update DashboardView to Use AppNavbar
- Import the new `AppNavbar` component
- Replace the inline navbar HTML (lines 3-21) with:
  ```vue
  <AppNavbar :show-profile-link="true" @logout="handleLogout" />
  ```
- Remove the duplicated navbar styles from the scoped CSS
- Keep the `handleLogout` function and auth composable imports

### Step 5: Update ProfileView to Use AppNavbar
- Import the new `AppNavbar` component
- Replace the inline navbar HTML (lines 3-11) with:
  ```vue
  <AppNavbar :show-dashboard-link="true" @logout="handleLogout" />
  ```
- Remove the duplicated navbar styles from the scoped CSS
- Keep the `handleLogout` function and auth composable imports

### Step 6: Run Validation Commands
- Execute all validation commands to ensure zero regressions
- Verify the favicon appears in browser tabs
- Verify the logo displays correctly in both Dashboard and Profile navbars
- Ensure logout functionality works from both views

## Validation Commands
Execute every command to validate the chore is complete with zero regressions.

- `cd app/client && npm run build` - Build the client to ensure no compilation errors
- `cd app/server && uv run pytest` - Run server tests to validate the chore is complete with zero regressions
- `docker compose build client` - Build the client Docker image to verify production build works

## Notes
- The logo provided shows a specific color scheme: blue (#3D3DBF or similar) for the icon frame and text, orange (#FF8C00 or similar) for the wave accents
- For best results, the logo SVG should be manually created or traced from the provided image to ensure crisp rendering at all sizes
- The Vite build process will automatically copy files from `public/` to the output directory
- Consider using a CSS variable or theme constant for the logo dimensions to maintain consistency
- The AppNavbar component should be designed to be reusable across any future views that need the standard navigation bar
- The existing gradient text style (`background: linear-gradient(135deg, #667eea 0%, #764ba2 100%)`) in the navbar brand should be removed in favor of the actual logo image

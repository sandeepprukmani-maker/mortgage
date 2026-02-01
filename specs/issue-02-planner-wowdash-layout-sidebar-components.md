# Plan: Create WowDash-Style Layout with Sidebar Navigation

## Description
Create a new layout system for the Valargen application that matches the WowDash admin dashboard template design. Based on the reference screenshots, the layout includes:

1. **Sidebar Navigation** - A vertical left sidebar (~250px wide) with:
   - Logo at the top with toggle arrow
   - Search input
   - Grouped menu items with icons (Dashboard, Application section with Customers, Users, Role & Access, etc.)
   - Collapsible menu groups
   - Active state highlighting (blue background for selected item)
   - If no route configured link to coming soon page

2. **Top Header Bar** - A horizontal header with:
   - Toggle arrow for sidebar collapse
   - Search input field
   - Right-side icons (theme toggle, language/flag, messages, notifications)
   - User profile avatar dropdown
   - Breadcrumb navigation on the right

3. **Main Content Area** - The page content area that:
   - Takes remaining width after sidebar
   - Has proper padding and max-width constraints
   - Displays page title and breadcrumb

4. **Color System Update** - Based on the color.html reference:
   - **Shades**: White (#FFFFFF), Dark (#111827)
   - **Neutral Scale**: 50 (#FAFAFA) through 900 (#171717)
   - **Primary Color Scale**: 50 (#E4F1FF) through 900 (#4536B6) - blue to purple gradient

The current application uses a simple top navbar only. This chore will create reusable layout components and refactor existing views to use the new sidebar layout and create blue theme, later theme could be customizable. Also the navigation should be smooth transition.

## Relevant Files
Use these files to resolve the chore:

- `app/client/src/style.css` - Current Tailwind theme configuration. Must be updated with the new WowDash color palette (neutral grays, primary blues).
- `app/client/src/App.vue` - Root application component. May need to integrate global layout components.
- `app/client/src/components/AppNavbar.vue` - Current top navigation bar. Will be replaced/refactored to work with new header component.
- `app/client/src/views/DashboardView.vue` - Dashboard page that will use the new layout.
- `app/client/src/views/CustomersView.vue` - Customers page that will use the new layout.
- `app/client/src/views/ProfileView.vue` - Profile page that will use the new layout.
- `app/client/src/views/LoginView.vue` - Login page (auth pages should NOT use sidebar layout).
- `app/client/src/router/index.js` - Router configuration to understand which routes need sidebar layout.
- `app/client/src/components/ui/BaseCard.vue` - Reference for slot-based component patterns.
- `app/client/src/components/ui/BaseButton.vue` - Reference for variant/size prop patterns.
- `resource/template/wowdash-vue-js-admin-dashboard-template-multipurpose/` - WowDash template reference for dashboard layout and components.

### New Files
The following new files will be created:

**Layout Components:**
- `app/client/src/layouts/DashboardLayout.vue` - Main layout with sidebar + header + content area
- `app/client/src/layouts/AuthLayout.vue` - Clean layout for login/register pages (no sidebar)

**Sidebar Components:**
- `app/client/src/components/sidebar/AppSidebar.vue` - Main sidebar container with logo and menu
- `app/client/src/components/sidebar/SidebarMenuItem.vue` - Individual menu item with icon
- `app/client/src/components/sidebar/SidebarMenuGroup.vue` - Collapsible menu group with children
- `app/client/src/components/sidebar/SidebarSearch.vue` - Search input in sidebar

**Header Components:**
- `app/client/src/components/header/AppHeader.vue` - Top header bar with actions
- `app/client/src/components/header/HeaderSearch.vue` - Search input in header
- `app/client/src/components/header/HeaderNotifications.vue` - Notifications dropdown
- `app/client/src/components/header/HeaderUserMenu.vue` - User profile dropdown
- `app/client/src/components/header/HeaderBreadcrumb.vue` - Breadcrumb navigation

**Store:**
- `app/client/src/stores/sidebar.js` - Pinia store for sidebar collapsed state

## Step by Step Tasks
IMPORTANT: Execute every step in order, top to bottom.

### Step 1: Update Color System in style.css
Update the Tailwind theme configuration with WowDash color palette:

- Replace current primary colors with WowDash Primary Blue scale:
  - `--color-primary-50: #E4F1FF`
  - `--color-primary-100: #BFDCFF`
  - `--color-primary-200: #95C7FF`
  - `--color-primary-300: #6BB1FF`
  - `--color-primary-400: #519FFF`
  - `--color-primary-500: #458EFF` (main primary)
  - `--color-primary-600: #487FFF` (slightly different, use for hover)
  - `--color-primary-700: #486CEA`
  - `--color-primary-800: #4759D6`
  - `--color-primary-900: #4536B6`

- Add Neutral color scale:
  - `--color-neutral-50: #FAFAFA`
  - `--color-neutral-100: #F5F5F5`
  - `--color-neutral-200: #E5E5E5`
  - `--color-neutral-300: #D4D4D4`
  - `--color-neutral-400: #A3A3A3`
  - `--color-neutral-500: #737373`
  - `--color-neutral-600: #525252`
  - `--color-neutral-700: #404040`
  - `--color-neutral-800: #262626`
  - `--color-neutral-900: #171717`

- Add Shades:
  - `--color-shade-white: #FFFFFF`
  - `--color-shade-dark: #111827`

### Step 2: Create Sidebar Store
Create `app/client/src/stores/sidebar.js`:

- State: `isCollapsed` (boolean), `isMobileOpen` (boolean for mobile overlay)
- Actions: `toggle()`, `collapse()`, `expand()`, `toggleMobile()`
- Getters: `sidebarWidth` (returns '250px' or '80px' based on collapsed state)
- Persist state to localStorage for user preference

### Step 3: Create Directory Structure
Create the following directories:
- `app/client/src/layouts/`
- `app/client/src/components/sidebar/`
- `app/client/src/components/header/`

### Step 4: Create SidebarMenuItem Component
Create `app/client/src/components/sidebar/SidebarMenuItem.vue`:

- Props: `to` (route path), `icon` (icon name/component), `label` (text), `badge` (optional count/text)
- Use `router-link` for navigation
- Active state detection using `$route.path`
- Styling:
  - Height: 44px
  - Padding: 12px 20px
  - Font: 15px, font-weight 500
  - Icon: 20x20px, margin-right 12px
  - Default: text-neutral-600, hover: bg-neutral-100
  - Active: bg-primary-50, text-primary-600, left border 3px primary-600
- Support collapsed mode (icon only, centered)

### Step 5: Create SidebarMenuGroup Component
Create `app/client/src/components/sidebar/SidebarMenuGroup.vue`:

- Props: `title` (group label), `icon` (optional), `defaultOpen` (boolean)
- State: `isOpen` (reactive, toggle on click)
- Styling:
  - Group header: uppercase, 11px font, text-neutral-400, letter-spacing 0.5px
  - Padding: 8px 20px
  - Chevron icon rotates on expand/collapse
- Slot for child menu items
- Animate height with Vue transition

### Step 6: Create SidebarSearch Component
Create `app/client/src/components/sidebar/SidebarSearch.vue`:

- Search input with magnifying glass icon
- Styling:
  - Background: neutral-100
  - Border-radius: 8px
  - Padding: 10px 12px
  - Font: 14px
  - Placeholder: "Search"
- Emit search event on input
- Hide when sidebar is collapsed

### Step 7: Create AppSidebar Component
Create `app/client/src/components/sidebar/AppSidebar.vue`:

- Import and use sidebar store for collapsed state
- Structure:
  - Logo section at top (router-link to /dashboard)
  - Toggle button (arrow icon) to collapse/expand
  - SidebarSearch component
  - Menu sections using SidebarMenuGroup and SidebarMenuItem
- Menu items based on current routes:
  - Dashboard (home icon) - /dashboard
  - Customers (users icon) - /customers
  - Profile (user icon) - /profile
- Styling:
  - Width: 250px (80px when collapsed)
  - Background: white
  - Border-right: 1px solid neutral-200
  - Position: fixed, left 0, top 0, height 100vh
  - Z-index: 40
  - Transition: width 300ms ease

### Step 8: Create HeaderBreadcrumb Component
Create `app/client/src/components/header/HeaderBreadcrumb.vue`:

- Props: `items` (array of {label, to?})
- Auto-generate from route if not provided
- Styling:
  - Font: 14px
  - Separator: "/" or ">"
  - Current page: text-neutral-600
  - Links: text-primary-600, hover underline

### Step 9: Create HeaderUserMenu Component
Create `app/client/src/components/header/HeaderUserMenu.vue`:

- Import user store for profile data
- Avatar display (BaseAvatar or initials)
- Dropdown menu on click:
  - Profile link
  - Settings link
  - Divider
  - Logout button
- Use existing logout logic from AppNavbar
- Styling:
  - Avatar: 36px round
  - Dropdown: white bg, shadow, rounded-lg, min-width 180px

### Step 10: Create HeaderNotifications Component
Create `app/client/src/components/header/HeaderNotifications.vue`:

- Bell icon button
- Badge showing unread count (if any)
- Dropdown with notification list (placeholder for now)
- Styling:
  - Icon button: 40px, rounded-full, hover bg-neutral-100
  - Badge: absolute positioned, red bg, white text, 18px

### Step 11: Create HeaderSearch Component
Create `app/client/src/components/header/HeaderSearch.vue`:

- Search input with icon
- Styling similar to SidebarSearch but adapted for header
- Width: 300px
- Background: neutral-100
- Border-radius: 50px (pill shape)

### Step 12: Create AppHeader Component
Create `app/client/src/components/header/AppHeader.vue`:

- Props: `title` (page title), `breadcrumbItems` (optional)
- Import sidebar store for toggle
- Structure:
  - Left: Toggle button (hamburger/arrow), HeaderSearch
  - Right: Theme toggle (placeholder), HeaderNotifications, HeaderUserMenu, HeaderBreadcrumb
- Styling:
  - Height: 70px
  - Background: white
  - Border-bottom: 1px solid neutral-200
  - Padding: 0 24px
  - Position: sticky, top 0
  - Z-index: 30

### Step 13: Create DashboardLayout Component
Create `app/client/src/layouts/DashboardLayout.vue`:

- Import AppSidebar, AppHeader, and sidebar store
- Structure:
  ```
  <div class="layout-wrapper">
    <AppSidebar />
    <div class="main-wrapper" :style="{ marginLeft: sidebarWidth }">
      <AppHeader :title="pageTitle" />
      <main class="content-wrapper">
        <slot />
      </main>
    </div>
  </div>
  ```
- Props: `pageTitle` (string), `maxWidth` ('full', '7xl', '3xl')
- Styling:
  - Main wrapper: min-height 100vh, background neutral-50
  - Content wrapper: padding 24px, max-width based on prop
  - Responsive: On mobile (<768px), sidebar becomes overlay

### Step 14: Create AuthLayout Component
Create `app/client/src/layouts/AuthLayout.vue`:

- Simple centered layout for auth pages
- No sidebar, full-screen gradient background
- Slot for auth form content
- Keep existing LoginView styling pattern

### Step 15: Refactor DashboardView to Use New Layout
Update `app/client/src/views/DashboardView.vue`:

- Wrap content in DashboardLayout component
- Remove AppNavbar import and usage
- Remove outer div with min-h-screen bg-gray-50
- Pass pageTitle="Dashboard" to layout
- Keep existing content structure

### Step 16: Refactor CustomersView to Use New Layout
Update `app/client/src/views/CustomersView.vue`:

- Wrap content in DashboardLayout component
- Remove AppNavbar import and usage
- Remove outer div with min-h-screen bg-gray-50
- Pass pageTitle="Customers" to layout
- Keep existing CustomerTable and PricingModal logic

### Step 17: Refactor ProfileView to Use New Layout
Update `app/client/src/views/ProfileView.vue`:

- Wrap content in DashboardLayout component
- Remove AppNavbar import and usage
- Remove outer div with min-h-screen bg-gray-50
- Pass pageTitle="Profile" and maxWidth="3xl" to layout
- Keep existing UserProfile component

### Step 18: Update Auth Views to Use AuthLayout (Optional)
Consider wrapping LoginView, RegisterView, ForgotPasswordView, ResetPasswordView with AuthLayout:

- Keep existing gradient and centered styling
- This is optional as auth pages already have their own layout

### Step 19: Remove or Deprecate AppNavbar
- AppNavbar.vue is no longer needed for authenticated pages
- Either delete the file or mark as deprecated
- Update any remaining imports

### Step 20: Run Validation Commands
Execute all validation commands to ensure zero regressions.

## Validation Commands
Execute every command to validate the chore is complete with zero regressions.

- `cd app/client && npm run build` - Build the client to check for compilation errors
- `cd app/client && npx vue-tsc --noEmit` - Run Vue TypeScript type checking (if TypeScript is used)
- `cd app/server && uv run pytest` - Run server tests to validate the chore is complete with zero regressions

## Notes

### Design Specifications from Screenshots

**Sidebar (from Screenshot 1):**
- Logo: "WowDash" with blue gradient icon
- Width: ~250px
- Background: White
- Menu item height: ~44px
- Active item: Light blue background (#E4F1FF), blue text, left blue border
- Icons: 20x20px, consistent spacing
- Section headers: Uppercase, small gray text

**Header (from Screenshot 1):**
- Height: ~70px
- Search: Pill-shaped input with gray background
- Right side: Flag icon, mail icon, bell icon, avatar
- Breadcrumb: "Dashboard" text on right

**Color Palette (from Screenshot 2):**
- The color system uses a 50-900 scale for both Neutral (grays) and Primary (blues)
- Primary 600 (#487FFF) appears to be the main action color
- Neutral 100 (#F5F5F5) is good for backgrounds
- Neutral 900 (#171717) for dark text

### Mobile Responsiveness
- On screens < 768px, sidebar should:
  - Be hidden by default
  - Slide in as overlay when toggle clicked
  - Have backdrop overlay
- Header should adjust search width
- Content should have reduced padding

### Component Architecture
- Follow existing patterns: defineProps, computed classes, slots
- Use Pinia store for sidebar state to share across components
- Keep components focused and single-responsibility
- Use existing BaseButton, BaseCard patterns where applicable

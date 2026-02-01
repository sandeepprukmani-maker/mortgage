# Plan: Implement TailwindCSS and Maximize Component Reusability

## Description
Implement TailwindCSS in the Vue 3 client application and refactor all existing components to use Tailwind utility classes instead of scoped CSS. Additionally, extract common UI patterns into reusable components to maximize code reuse and maintain consistency across the application.

The current codebase uses scoped CSS with repeated styling patterns across 15 Vue components. This chore will:
1. Install and configure TailwindCSS with Vite
2. Create reusable UI components for common patterns (buttons, inputs, cards, badges, alerts)
3. Refactor all existing components to use TailwindCSS utility classes
4. Remove all scoped CSS styles in favor of Tailwind classes
5. Maintain the existing visual design while improving maintainability

## Relevant Files
Use these files to resolve the chore:

### Configuration Files
- **`app/client/package.json`** - Add TailwindCSS and related dependencies
- **`app/client/vite.config.js`** - May need postcss configuration (Vite auto-detects postcss.config.js)
- **`app/client/src/main.js`** - Import Tailwind CSS file
- **`app/client/src/style.css`** - Replace with Tailwind directives
- **`app/client/src/App.vue`** - Remove global styles, use Tailwind base

### Existing Components to Refactor
- **`app/client/src/components/AppNavbar.vue`** - Navbar with logo, links, logout button (150 lines of scoped CSS)
- **`app/client/src/components/LoginForm.vue`** - Form with inputs, buttons, error messages (94 lines of scoped CSS)
- **`app/client/src/components/RegisterForm.vue`** - Form with more complex layout (117 lines of scoped CSS)
- **`app/client/src/components/ForgotPasswordForm.vue`** - Similar form pattern
- **`app/client/src/components/ResetPasswordForm.vue`** - Similar form pattern
- **`app/client/src/components/GoogleLoginButton.vue`** - Social login button (32 lines of scoped CSS)
- **`app/client/src/components/UserProfile.vue`** - Profile card with avatar, badges, details (140 lines of scoped CSS)

### Existing Views to Refactor
- **`app/client/src/views/LoginView.vue`** - Auth layout with gradient background (60 lines of scoped CSS)
- **`app/client/src/views/RegisterView.vue`** - Similar auth layout
- **`app/client/src/views/ForgotPasswordView.vue`** - Similar auth layout
- **`app/client/src/views/ResetPasswordView.vue`** - Similar auth layout
- **`app/client/src/views/OAuthCallbackView.vue`** - Loading/callback view
- **`app/client/src/views/DashboardView.vue`** - Dashboard with cards, modules grid (188 lines of scoped CSS)
- **`app/client/src/views/ProfileView.vue`** - Profile page layout (33 lines of scoped CSS)

### New Files
- **`app/client/tailwind.config.js`** - Tailwind configuration with custom theme
- **`app/client/postcss.config.js`** - PostCSS configuration for Tailwind
- **`app/client/src/components/ui/BaseButton.vue`** - Reusable button component with variants (primary, secondary, danger, outline)
- **`app/client/src/components/ui/BaseInput.vue`** - Reusable input component with label, error, help text
- **`app/client/src/components/ui/BaseCard.vue`** - Reusable card component with header/body/footer slots
- **`app/client/src/components/ui/BaseBadge.vue`** - Reusable badge component with variants
- **`app/client/src/components/ui/BaseAlert.vue`** - Reusable alert component for success/error/warning messages
- **`app/client/src/components/ui/BaseAvatar.vue`** - Reusable avatar component with initials fallback
- **`app/client/src/components/ui/BaseDivider.vue`** - Reusable divider component with optional text
- **`app/client/src/components/ui/BaseIcon.vue`** - Wrapper for SVG icons with consistent sizing
- **`app/client/src/components/ui/index.js`** - Barrel export for all UI components

## Step by Step Tasks
IMPORTANT: Execute every step in order, top to bottom.

### Step 1: Install TailwindCSS Dependencies
- Run `npm install -D tailwindcss postcss autoprefixer` in the `app/client` directory
- Run `npx tailwindcss init -p` to generate `tailwind.config.js` and `postcss.config.js`

### Step 2: Configure TailwindCSS
- Update `app/client/tailwind.config.js` with:
  ```javascript
  /** @type {import('tailwindcss').Config} */
  export default {
    content: [
      "./index.html",
      "./src/**/*.{vue,js,ts,jsx,tsx}",
    ],
    theme: {
      extend: {
        colors: {
          primary: {
            50: '#eef2ff',
            100: '#e0e7ff',
            200: '#c7d2fe',
            300: '#a5b4fc',
            400: '#818cf8',
            500: '#667eea',
            600: '#5b6ce0',
            700: '#4f5bd5',
            800: '#4338ca',
            900: '#3730a3',
          },
          brand: {
            purple: '#764ba2',
            blue: '#3D3DBF',
            orange: '#FF8C00',
          }
        },
        fontFamily: {
          sans: ['-apple-system', 'BlinkMacSystemFont', 'Segoe UI', 'Roboto', 'Helvetica Neue', 'Arial', 'sans-serif'],
        },
        boxShadow: {
          'card': '0 1px 3px rgba(0, 0, 0, 0.1)',
          'card-hover': '0 4px 6px rgba(102, 126, 234, 0.1)',
        },
      },
    },
    plugins: [],
  }
  ```
- Ensure `postcss.config.js` has:
  ```javascript
  export default {
    plugins: {
      tailwindcss: {},
      autoprefixer: {},
    },
  }
  ```

### Step 3: Update Global Styles
- Replace `app/client/src/style.css` content with Tailwind directives:
  ```css
  @tailwind base;
  @tailwind components;
  @tailwind utilities;

  @layer base {
    body {
      @apply font-sans antialiased;
    }
  }
  ```
- Update `app/client/src/App.vue` to remove the `<style>` block entirely (styles will come from Tailwind)
- Ensure `app/client/src/main.js` still imports `./style.css`

### Step 4: Create Base UI Components Directory
- Create the directory `app/client/src/components/ui/`
- Create the barrel export file `app/client/src/components/ui/index.js`

### Step 5: Create BaseButton Component
- Create `app/client/src/components/ui/BaseButton.vue` with:
  - Props: `variant` (primary|secondary|danger|outline|google), `size` (sm|md|lg), `disabled`, `loading`, `type`
  - Slot for button content
  - Tailwind classes for all variants matching existing design
  - Loading spinner support

### Step 6: Create BaseInput Component
- Create `app/client/src/components/ui/BaseInput.vue` with:
  - Props: `modelValue`, `label`, `type`, `placeholder`, `disabled`, `error`, `helpText`, `id`
  - v-model support via emit
  - Label rendering
  - Error message display
  - Help text display
  - Tailwind classes matching existing input styles

### Step 7: Create BaseCard Component
- Create `app/client/src/components/ui/BaseCard.vue` with:
  - Props: `padding` (default: true), `shadow` (default: true)
  - Named slots: header, default (body), footer
  - Tailwind classes for card styling

### Step 8: Create BaseBadge Component
- Create `app/client/src/components/ui/BaseBadge.vue` with:
  - Props: `variant` (default|primary|success|warning|danger|role|provider|plan)
  - Slot for badge content
  - Tailwind classes matching existing badge styles

### Step 9: Create BaseAlert Component
- Create `app/client/src/components/ui/BaseAlert.vue` with:
  - Props: `variant` (error|success|warning|info)
  - Slot for alert content
  - Tailwind classes matching existing error-message and success-message styles

### Step 10: Create BaseAvatar Component
- Create `app/client/src/components/ui/BaseAvatar.vue` with:
  - Props: `firstName`, `lastName`, `size` (sm|md|lg|xl), `src` (optional image)
  - Computed initials from names
  - Tailwind classes matching existing avatar style

### Step 11: Create BaseDivider Component
- Create `app/client/src/components/ui/BaseDivider.vue` with:
  - Props: `text` (optional)
  - Slot for custom content
  - Tailwind classes matching existing divider style (OR in auth views)

### Step 12: Create BaseIcon Component
- Create `app/client/src/components/ui/BaseIcon.vue` with:
  - Props: `name` (icon identifier), `size` (sm|md|lg)
  - Wrapper for consistent icon sizing
  - Uses named slots for custom SVG content

### Step 13: Update Barrel Export
- Update `app/client/src/components/ui/index.js` to export all components:
  ```javascript
  export { default as BaseButton } from './BaseButton.vue'
  export { default as BaseInput } from './BaseInput.vue'
  export { default as BaseCard } from './BaseCard.vue'
  export { default as BaseBadge } from './BaseBadge.vue'
  export { default as BaseAlert } from './BaseAlert.vue'
  export { default as BaseAvatar } from './BaseAvatar.vue'
  export { default as BaseDivider } from './BaseDivider.vue'
  export { default as BaseIcon } from './BaseIcon.vue'
  ```

### Step 14: Refactor AppNavbar Component
- Replace all scoped CSS with Tailwind utility classes
- Use `class` attributes with Tailwind classes
- Remove the entire `<style scoped>` block
- Example navbar classes: `bg-white shadow-card px-8 py-4 flex justify-between items-center`

### Step 15: Refactor LoginForm Component
- Import and use `BaseInput`, `BaseButton`, `BaseAlert` components
- Replace form-group styling with Tailwind flexbox utilities
- Replace `.btn-primary` with `<BaseButton variant="primary">`
- Replace error/success messages with `<BaseAlert>`
- Remove the entire `<style scoped>` block

### Step 16: Refactor RegisterForm Component
- Import and use `BaseInput`, `BaseButton`, `BaseAlert` components
- Use Tailwind grid for form-row layout: `grid grid-cols-2 gap-4 sm:grid-cols-1`
- Replace all form elements with base components
- Remove the entire `<style scoped>` block

### Step 17: Refactor ForgotPasswordForm Component
- Apply same refactoring pattern as LoginForm
- Use base components for inputs, buttons, alerts
- Remove the entire `<style scoped>` block

### Step 18: Refactor ResetPasswordForm Component
- Apply same refactoring pattern as LoginForm
- Use base components for inputs, buttons, alerts
- Remove the entire `<style scoped>` block

### Step 19: Refactor GoogleLoginButton Component
- Use `<BaseButton variant="google">` or custom Tailwind classes
- Keep the Google SVG icon inline
- Remove the entire `<style scoped>` block

### Step 20: Refactor UserProfile Component
- Import and use `BaseCard`, `BaseBadge`, `BaseAvatar`, `BaseAlert` components
- Replace profile-card with `<BaseCard>`
- Replace avatar with `<BaseAvatar :first-name="..." :last-name="...">`
- Replace badges with `<BaseBadge variant="...">`
- Replace error-message with `<BaseAlert variant="error">`
- Use Tailwind gradient for profile header: `bg-gradient-to-br from-primary-500 to-brand-purple`
- Remove the entire `<style scoped>` block

### Step 21: Refactor LoginView
- Use Tailwind utility classes for auth layout
- Background gradient: `min-h-screen flex items-center justify-center bg-gradient-to-br from-primary-500 to-brand-purple p-4`
- Auth card: `bg-white rounded-2xl shadow-xl p-10 w-full max-w-md`
- Use `<BaseDivider text="OR" />` for the divider
- Remove the entire `<style scoped>` block

### Step 22: Refactor RegisterView
- Apply same auth layout pattern as LoginView
- Remove the entire `<style scoped>` block

### Step 23: Refactor ForgotPasswordView
- Apply same auth layout pattern as LoginView
- Remove the entire `<style scoped>` block

### Step 24: Refactor ResetPasswordView
- Apply same auth layout pattern as LoginView
- Remove the entire `<style scoped>` block

### Step 25: Refactor OAuthCallbackView
- Use Tailwind classes for loading/callback styling
- Remove any scoped CSS

### Step 26: Refactor DashboardView
- Use Tailwind classes for dashboard layout
- Main container: `min-h-screen bg-gray-50`
- Dashboard container: `max-w-7xl mx-auto p-8`
- Grid layout: `grid grid-cols-1 lg:grid-cols-[1fr_1.5fr] gap-8`
- Info cards: Use `<BaseCard>` with icon and content
- Module cards: Use Tailwind for hover effects and transitions
- Remove the entire `<style scoped>` block

### Step 27: Refactor ProfileView
- Use Tailwind classes for profile layout
- Import and use `<AppNavbar>` (already done)
- Container: `min-h-screen bg-gray-50`
- Profile container: `max-w-3xl mx-auto p-8`
- Remove the entire `<style scoped>` block

### Step 28: Run Validation Commands
- Execute all validation commands to ensure zero regressions
- Verify the application builds successfully
- Verify all styles render correctly matching the original design

## Validation Commands
Execute every command to validate the chore is complete with zero regressions.

- `cd app/client && npm install` - Install all dependencies including TailwindCSS
- `cd app/client && npm run build` - Build the client to ensure no compilation errors and Tailwind is working
- `cd app/server && uv run pytest` - Run server tests to validate no regressions

## Notes
- The existing color palette uses:
  - Primary gradient: `#667eea` to `#764ba2`
  - Blue accent: `#3b82f6`
  - Gray scale: `#1f2937`, `#374151`, `#4b5563`, `#6b7280`, `#9ca3af`, `#d1d5db`, `#e5e7eb`, `#f3f4f6`, `#f9fafb`
  - Red for errors/danger: `#ef4444`, `#dc2626`
  - Green for success: `#059669`, `#065f46`, `#d1fae5`
  - Brand colors from logo: Blue `#3D3DBF`, Orange `#FF8C00`

- Common patterns to extract:
  - Form groups (label + input + error)
  - Primary/Secondary/Danger buttons
  - Card with shadow and rounded corners
  - Error and success alert messages
  - Badge/pill components
  - Avatar with initials
  - OR divider for auth forms

- When refactoring, ensure:
  - All hover states are preserved
  - All disabled states are preserved
  - All responsive breakpoints are preserved
  - All transitions/animations are preserved
  - The visual appearance matches the original design exactly

- TailwindCSS class organization recommendation:
  - Layout classes first (flex, grid, position)
  - Spacing classes (margin, padding)
  - Sizing classes (width, height)
  - Typography classes (font, text)
  - Background/border classes
  - State classes (hover:, focus:, disabled:)

# Plan: Apply WowDash Authentication Design to Login and Signup Pages

## Metadata

## Description
Apply the WowDash admin template authentication design to the existing login and signup pages. The goal is to transform the current minimalist authentication pages to match the WowDash authentication design which features:
- Split-screen layout with decorative left panel and form on right
- WowDash styling (Bootstrap-inspired utility classes with custom CSS variables)
- Icon fields for form inputs using iconify-icon
- Password visibility toggle
- Social login buttons (Google, Facebook - but only Google functional)
- "Remember me" checkbox on login
- Terms & conditions checkbox on signup
- Consistent styling with the rest of the WowDash-styled dashboard

The existing authentication logic (useAuth composable, API calls, validation) must be preserved while updating only the UI/design.

## Relevant Files
Use these files to resolve the chore:

**Template Reference Files (read-only):**
- `resource/template/wowdash-vue-js-admin-dashboard-template-multipurpose/wowdash-admin/src/components/Authentication/SignIn.vue` - WowDash sign-in component template to copy design from
- `resource/template/wowdash-vue-js-admin-dashboard-template-multipurpose/wowdash-admin/src/components/Authentication/SignUp.vue` - WowDash sign-up component template to copy design from
- `resource/template/wowdash-vue-js-admin-dashboard-template-multipurpose/wowdash-admin/src/components/Authentication/ForgotPassword.vue` - WowDash forgot password template for design reference
- `resource/template/wowdash-vue-js-admin-dashboard-template-multipurpose/wowdash-admin/src/assets/css/style.css` - WowDash CSS (lines 14008-14053 contain auth-specific styles)
- `resource/template/wowdash-vue-js-admin-dashboard-template-multipurpose/wowdash-admin/src/assets/images/auth/auth-img.png` - Decorative image for sign-in/sign-up left panel
- `resource/template/wowdash-vue-js-admin-dashboard-template-multipurpose/wowdash-admin/src/assets/images/auth/forgot-pass-img.png` - Decorative image for forgot password left panel
- `resource/template/wowdash-vue-js-admin-dashboard-template-multipurpose/wowdash-admin/src/assets/images/logo.png` - Logo for auth pages

**Existing App Files to Modify:**
- `app/client/src/views/LoginView.vue` - Main login view to redesign with WowDash layout
- `app/client/src/views/RegisterView.vue` - Main register view to redesign with WowDash layout
- `app/client/src/views/ForgotPasswordView.vue` - Forgot password view to redesign
- `app/client/src/views/ResetPasswordView.vue` - Reset password view to redesign
- `app/client/src/components/LoginForm.vue` - Login form component to integrate into new design
- `app/client/src/components/RegisterForm.vue` - Register form component to integrate into new design
- `app/client/src/components/ForgotPasswordForm.vue` - Forgot password form to integrate
- `app/client/src/components/ResetPasswordForm.vue` - Reset password form to integrate
- `app/client/src/components/GoogleLoginButton.vue` - Google OAuth button to style consistently
- `app/client/src/style.css` - Main stylesheet to add WowDash auth CSS

**Existing Logic Files (do not modify - only reference):**
- `app/client/src/composables/useAuth.js` - Authentication logic to preserve
- `app/client/src/composables/useGoogleAuth.js` - Google OAuth logic to preserve
- `app/client/src/router/index.js` - Routing configuration (no changes needed)

### New Files
- `app/client/src/assets/images/auth/auth-img.png` - Copy from WowDash template
- `app/client/src/assets/images/auth/forgot-pass-img.png` - Copy from WowDash template
- `app/client/src/assets/images/logo.png` - Copy from WowDash template (or use existing Valargen logo if available)

## Step by Step Tasks
IMPORTANT: Execute every step in order, top to bottom.

### Step 1: Copy Required Assets
- Create directory `app/client/src/assets/images/auth/` if it doesn't exist
- Copy `auth-img.png` from `resource/template/wowdash-vue-js-admin-dashboard-template-multipurpose/wowdash-admin/src/assets/images/auth/auth-img.png` to `app/client/src/assets/images/auth/`
- Copy `forgot-pass-img.png` from `resource/template/wowdash-vue-js-admin-dashboard-template-multipurpose/wowdash-admin/src/assets/images/auth/forgot-pass-img.png` to `app/client/src/assets/images/auth/`
- Copy `logo.png` from `resource/template/wowdash-vue-js-admin-dashboard-template-multipurpose/wowdash-admin/src/assets/images/logo.png` to `app/client/src/assets/images/` (if no existing logo)

### Step 2: Add WowDash Authentication CSS to style.css
- Add the WowDash authentication CSS to `app/client/src/style.css`
- Include the `.auth`, `.auth-left`, `.auth-right` styles
- Include the `.center-border-horizontal` style for dividers
- Include the `.icon-field` styles for form inputs with icons
- Include the `.form-control`, `.h-56-px`, `.bg-neutral-50`, `.radius-12` utility classes
- Include responsive media queries for auth pages
- Ensure CSS variables for colors match WowDash theme (already in place from previous work)

### Step 3: Redesign LoginView.vue
- Replace the current centered card layout with WowDash split-screen layout
- Add `.auth` section with `.auth-left` (decorative image panel) and `.auth-right` (form panel)
- Include logo at top of form area
- Add title "Sign In to your Account" and subtitle
- Replace BaseInput components with WowDash icon-field styled inputs for email and password
- Add password visibility toggle using eye icon
- Add "Remember me" checkbox with proper styling
- Add "Forgot Password?" link
- Keep the GoogleLoginButton but style it to match WowDash social buttons
- Add "Or sign in with" divider using `.center-border-horizontal`
- Add Facebook button (non-functional placeholder) alongside Google button
- Add "Don't have an account? Sign Up" link at bottom
- Preserve all existing login logic from useAuth composable
- Add loading states and error handling display

### Step 4: Redesign RegisterView.vue
- Replace the current centered card layout with WowDash split-screen layout
- Add `.auth` section with `.auth-left` (decorative image panel) and `.auth-right` (form panel)
- Include logo at top of form area
- Add title "Sign Up to your Account" and subtitle
- Replace BaseInput components with WowDash icon-field styled inputs:
  - First name (person icon)
  - Last name (person icon)
  - Email (email icon)
  - Password (lock icon) with visibility toggle
  - Confirm password (lock icon) with visibility toggle
- Add terms & conditions checkbox with links
- Add password requirement hint text
- Keep the GoogleLoginButton but style it to match WowDash social buttons
- Add "Or sign up with" divider
- Add Facebook button (non-functional) alongside Google button
- Add "Already have an account? Sign In" link at bottom
- Preserve all existing registration logic and validation from useAuth composable
- Add loading states, success/error message display

### Step 5: Redesign ForgotPasswordView.vue
- Replace current layout with WowDash split-screen layout
- Use `.auth.forgot-password-page` class for different gradient background on left panel
- Use `forgot-pass-img.png` for left panel image
- Add title "Forgot Password" and descriptive subtitle
- Add email input with icon field styling
- Add "Continue" / "Send Reset Link" button
- Add "Back to Sign In" link
- Preserve existing forgot password logic from useAuth
- Display success/error messages appropriately

### Step 6: Redesign ResetPasswordView.vue
- Apply similar WowDash styling as forgot password page
- Add password input with icon and visibility toggle
- Add confirm password input with icon and visibility toggle
- Add password requirement hint text
- Add "Reset Password" button
- Add "Back to Sign In" link
- Preserve existing reset password logic and validation
- Display success/error messages and redirect on success

### Step 7: Update GoogleLoginButton.vue Styling
- Update the button to match WowDash social button styling
- Use WowDash button classes: `fw-semibold text-primary-light py-16 px-24 w-50 border radius-12`
- Keep the Google SVG icon
- Ensure consistent hover states with WowDash design
- Preserve existing Google OAuth logic from useGoogleAuth

### Step 8: Clean Up Unused Components
- Review if LoginForm.vue, RegisterForm.vue, ForgotPasswordForm.vue, ResetPasswordForm.vue are still needed
- If the form logic is now embedded directly in the view components, consider removing the separate form components
- Alternatively, refactor to keep forms as separate components but with new WowDash styling

### Step 9: Run Validation
- Run build to check for TypeScript/compilation errors
- Run linter to check for code style issues
- Manually test all authentication flows:
  - Login with email/password
  - Login with Google OAuth
  - Registration with all fields
  - Forgot password flow
  - Reset password flow
  - Logout
- Verify responsive design on mobile breakpoints
- Verify dark mode compatibility (if applicable)

## Validation Commands
Execute every command to validate the chore is complete with zero regressions.

- `cd app/server && uv run pytest` - Run server tests to validate backend is unaffected
- `cd app/client && bun run build` - Build client to check for compilation errors
- `cd app/client && npx vue-tsc --noEmit` - Type check Vue components (if TypeScript is configured)

## Notes

- The WowDash template uses Bootstrap utility classes (d-flex, justify-content-center, etc.) and custom CSS. Since the app uses Tailwind, we'll need to either:
  1. Add the required Bootstrap-like utility classes to style.css, OR
  2. Convert WowDash Bootstrap classes to Tailwind equivalents
  - Recommendation: Add minimal required custom CSS classes to avoid major refactoring

- The WowDash template uses `iconify-icon` web component for icons. Check if this is already installed in the project. If not, add it:
  ```bash
  cd app/client && bun add iconify-icon
  ```
  And import in main.js: `import 'iconify-icon'`

- The "Remember me" checkbox functionality is UI-only in the template. If persistence is needed, implement localStorage for email or extend token expiry.

- The Facebook login button should be styled but non-functional (placeholder for future implementation).

- The existing BaseInput, BaseButton, BaseAlert components can still be used internally if needed, but the visible styling should match WowDash design.

- Password visibility toggle should use the `ri-eye-line` / `ri-eye-off-line` icons from Remix Icon (included in WowDash) or equivalent iconify icons.

- Error messages should be displayed inline below forms or as alerts, matching WowDash styling patterns.

- The auth pages should work without the dashboard sidebar/header layout - they are standalone full-page layouts.

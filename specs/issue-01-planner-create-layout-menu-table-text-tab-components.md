# Plan: Create Layout, Menu, Table, Text, Tab Components (WowDash Reference)

## Description
Create a set of reusable UI components for the Valargen Vue 3 frontend application, inspired by the WowDash Vue admin dashboard template. The components to create are:

1. **Layout Components** - Reusable page layouts with sidebar and main content areas
2. **Menu Components** - Sidebar navigation menu with collapsible sections, icons, and active states
3. **Table Components** - Enhanced data table with sorting, pagination, filtering, and customizable columns
4. **Text Components** - Typography components for consistent text styling (headings, paragraphs, labels)
5. **Tab Components** - Tabbed interface component using Vue 3 Composition API with provide/inject pattern

These components will follow the existing codebase patterns (Vue 3 Composition API, Tailwind CSS, slot-based architecture) and integrate with the current design system defined in `app/client/src/style.css`.

## Relevant Files
Use these files to resolve the chore:

- `app/client/src/style.css` - Contains the Tailwind CSS theme configuration with color variables, shadows, and font definitions. New components should use these theme tokens.
- `app/client/src/components/ui/BaseCard.vue` - Reference for slot-based component architecture with header/footer slots and prop-based styling.
- `app/client/src/components/ui/BaseButton.vue` - Reference for variant/size patterns using computed classes.
- `app/client/src/components/ui/BaseInput.vue` - Reference for form input styling and v-model binding.
- `app/client/src/components/ui/BaseAlert.vue` - Reference for variant-based styling patterns.
- `app/client/src/components/ui/BaseBadge.vue` - Reference for small inline components with variants.
- `app/client/src/components/ui/BaseIcon.vue` - Reference for size-based icon wrapper.
- `app/client/src/components/CustomerTable.vue` - Current table implementation to enhance/reference for BaseTable component.
- `app/client/src/components/AppNavbar.vue` - Current navigation implementation to reference for menu patterns.
- `app/client/src/views/DashboardView.vue` - Reference for page structure patterns to abstract into layout components.
- `app/client/src/views/ProfileView.vue` - Reference for page structure with different content width.
- `app/client/src/views/CustomersView.vue` - Reference for page structure with full-width content.
- `app/client/src/App.vue` - Root application structure showing global component usage.
- `app/client/src/router/index.js` - Router configuration to understand navigation structure.

### New Files
The following new files will be created:

**Layout Components:**
- `app/client/src/components/ui/layouts/BaseLayout.vue` - Main layout wrapper with sidebar support
- `app/client/src/components/ui/layouts/PageHeader.vue` - Reusable page header with title and subtitle

**Menu Components:**
- `app/client/src/components/ui/menu/SidebarMenu.vue` - Sidebar navigation container
- `app/client/src/components/ui/menu/SidebarMenuItem.vue` - Individual menu item with icon support
- `app/client/src/components/ui/menu/SidebarMenuGroup.vue` - Collapsible menu group

**Table Components:**
- `app/client/src/components/ui/table/BaseTable.vue` - Core table component with slots
- `app/client/src/components/ui/table/TableHeader.vue` - Table header with sorting capability
- `app/client/src/components/ui/table/TablePagination.vue` - Pagination controls
- `app/client/src/components/ui/table/TableEmpty.vue` - Empty state display
- `app/client/src/components/ui/table/TableLoading.vue` - Loading overlay

**Text Components:**
- `app/client/src/components/ui/typography/BaseHeading.vue` - Heading component (h1-h6)
- `app/client/src/components/ui/typography/BaseText.vue` - Paragraph/text component
- `app/client/src/components/ui/typography/BaseLabel.vue` - Form label component

**Tab Components:**
- `app/client/src/components/ui/tabs/BaseTabs.vue` - Tab container with provide/inject
- `app/client/src/components/ui/tabs/BaseTab.vue` - Individual tab content panel
- `app/client/src/components/ui/tabs/BaseTabList.vue` - Tab button list

## Step by Step Tasks
IMPORTANT: Execute every step in order, top to bottom.

### Step 1: Create Directory Structure
- Create the following directories under `app/client/src/components/ui/`:
  - `layouts/`
  - `menu/`
  - `table/`
  - `typography/`
  - `tabs/`

### Step 2: Create Typography Components (Foundation)
Typography components are foundational and will be used by other components.

- **BaseHeading.vue**: Create heading component with:
  - Props: `level` (1-6), `size` (sm, md, lg, xl, 2xl, 3xl), `weight` (normal, medium, semibold, bold), `color` (gray-800 default)
  - Use semantic heading tags (h1-h6) based on level prop
  - Apply Tailwind classes for text sizing and font weight
  - Support slot for content

- **BaseText.vue**: Create paragraph/text component with:
  - Props: `size` (xs, sm, base, lg), `color` (gray-600 default), `weight` (normal, medium)
  - Props: `as` (p, span, div) for element type flexibility
  - Apply consistent text styling with Tailwind

- **BaseLabel.vue**: Create label component with:
  - Props: `for` (input id), `required` (boolean), `size` (sm, md)
  - Show asterisk indicator when required
  - Use font-medium text-gray-700 styling (consistent with BaseInput)

### Step 3: Create Tab Components
Tab components use Vue 3 provide/inject for parent-child communication.

- **BaseTabs.vue**: Create tab container with:
  - Props: `modelValue` (active tab index or key), `variant` (underline, boxed, pills)
  - State: Track selected tab, register/unregister tabs via provide
  - Provide: `registerTab`, `unregisterTab`, `selectedTab`, `selectTab` methods
  - Emit: `update:modelValue` for v-model support
  - Render tab list and tab panels using slots

- **BaseTabList.vue**: Create tab button list with:
  - Inject parent context from BaseTabs
  - Render tab buttons with proper aria attributes
  - Support keyboard navigation (arrow keys)
  - Apply variant-specific styling (underline border-b, boxed bg, pills rounded)

- **BaseTab.vue**: Create individual tab panel with:
  - Props: `name` (tab identifier), `title` (display text), `disabled` (boolean), `icon` (optional slot)
  - Inject parent context to register/unregister
  - Use onMounted/onUnmounted for lifecycle registration
  - Show/hide content based on selected state
  - Support lazy rendering option

### Step 4: Create Table Components
Build enhanced table components with sorting, pagination, and filtering.

- **TableLoading.vue**: Create loading overlay with:
  - Props: `message` (loading text)
  - Absolute positioned overlay with spinner animation
  - Consistent with existing loading patterns in CustomerTable

- **TableEmpty.vue**: Create empty state component with:
  - Props: `icon` (slot), `title`, `description`
  - Centered layout with icon, heading, and text
  - Default icon slot with users icon

- **TableHeader.vue**: Create sortable header cell with:
  - Props: `sortable` (boolean), `sortKey` (string), `currentSort` (object), `align` (left, center, right)
  - Emit: `sort` event with sort key and direction
  - Show sort indicator icons (up/down arrows)
  - Apply bg-gray-50 and uppercase styling

- **TablePagination.vue**: Create pagination controls with:
  - Props: `total`, `perPage`, `currentPage`, `showPageSize` (boolean)
  - Emit: `page-change`, `page-size-change`
  - Display page info: "Showing X to Y of Z entries"
  - Previous/Next buttons with disabled states
  - Optional page size selector (10, 25, 50, 100)

- **BaseTable.vue**: Create main table component with:
  - Props: `columns` (array with key, label, sortable, align, width), `data` (array), `loading`, `emptyTitle`, `emptyDescription`, `sortKey`, `sortDirection`, `selectable`
  - Slots: `header`, `row`, `cell-{key}`, `empty`, `loading`
  - Features: Column-based rendering, row hover states, optional row selection
  - Integrate TableLoading, TableEmpty, TableHeader components
  - Apply min-w-full divide-y divide-gray-200 styling

### Step 5: Create Menu Components
Build sidebar navigation components with collapsible groups.

- **SidebarMenuItem.vue**: Create individual menu item with:
  - Props: `to` (route path), `icon` (slot), `label`, `badge` (optional), `active` (boolean or auto-detect from route)
  - Use router-link for navigation
  - Apply active state styling (text-primary-600, bg-primary-50)
  - Support icon slot on the left
  - Show optional badge on the right

- **SidebarMenuGroup.vue**: Create collapsible menu group with:
  - Props: `title`, `icon` (slot), `defaultOpen` (boolean)
  - State: Track expanded/collapsed state
  - Transition: Smooth height animation on expand/collapse
  - Render chevron icon that rotates based on state
  - Slot for child SidebarMenuItem components

- **SidebarMenu.vue**: Create sidebar container with:
  - Props: `collapsed` (boolean), `width` (default 256px), `collapsedWidth` (64px)
  - Slots: `header` (logo area), `footer` (user info), `default` (menu items)
  - Apply fixed positioning with proper z-index
  - Support collapse animation with width transition
  - Apply bg-white border-r border-gray-200 styling

### Step 6: Create Layout Components
Build page layout components that integrate navigation.

- **PageHeader.vue**: Create page header with:
  - Props: `title`, `subtitle`
  - Slots: `actions` (for buttons), `breadcrumb`
  - Apply mb-8 spacing, text-3xl for title, text-gray-500 for subtitle
  - Consistent with existing view headers

- **BaseLayout.vue**: Create main layout wrapper with:
  - Props: `sidebar` (boolean), `maxWidth` (sm, md, lg, xl, 2xl, 7xl, full), `padded` (boolean)
  - Slots: `sidebar`, `header`, `default` (main content)
  - Integrate with SidebarMenu when sidebar prop is true
  - Apply min-h-screen bg-gray-50 base styling
  - Responsive padding (p-4 md:p-8)
  - Support AppNavbar integration via header slot

### Step 7: Create Component Index Files
Create index.js export files for each component category.

- `app/client/src/components/ui/layouts/index.js` - Export BaseLayout, PageHeader
- `app/client/src/components/ui/menu/index.js` - Export SidebarMenu, SidebarMenuItem, SidebarMenuGroup
- `app/client/src/components/ui/table/index.js` - Export BaseTable, TableHeader, TablePagination, TableEmpty, TableLoading
- `app/client/src/components/ui/typography/index.js` - Export BaseHeading, BaseText, BaseLabel
- `app/client/src/components/ui/tabs/index.js` - Export BaseTabs, BaseTabList, BaseTab

### Step 8: Update CustomerTable to Use New Components (Optional Refactor)
- Refactor CustomerTable.vue to use the new BaseTable component
- Extract loading and empty states to use TableLoading and TableEmpty
- This validates the new components work correctly with existing data

### Step 9: Run Validation Commands
Execute all validation commands to ensure zero regressions.

## Validation Commands
Execute every command to validate the chore is complete with zero regressions.

- `cd app/client && npm run build` - Build the client to check for TypeScript/compilation errors
- `cd app/client && npx vue-tsc --noEmit` - Run Vue TypeScript type checking
- `cd app/server && uv run pytest` - Run server tests to validate the chore is complete with zero regressions

## Notes

### Design System Alignment
All components should use the theme tokens defined in `style.css`:
- Primary colors: `--color-primary-*` (50-900 scale)
- Shadows: `--shadow-card`, `--shadow-card-hover`
- Font: System font stack defined in `--font-family-sans`

### Component Architecture Patterns
Follow existing patterns:
- Use `defineProps()` with validators for type safety
- Use `computed()` for dynamic class strings
- Use `emit()` for parent communication
- Use slots for flexible content injection
- Use provide/inject for nested component communication (tabs)

### Tailwind CSS Conventions
- Use utility classes directly in templates
- Extract repeated patterns to computed properties
- Use conditional classes with object syntax or array join pattern
- Follow mobile-first responsive design (base → md: → lg:)

### Accessibility Considerations
- Use semantic HTML elements (nav, main, header, etc.)
- Include proper ARIA attributes for interactive components
- Support keyboard navigation for tabs and menus
- Ensure sufficient color contrast for text elements

### WowDash Reference
While we cannot directly access WowDash source code, the components are inspired by modern admin dashboard patterns:
- Clean, minimal design with consistent spacing
- Utility-first CSS approach with Tailwind
- Component-based architecture with slots for flexibility
- Responsive design that works across device sizes

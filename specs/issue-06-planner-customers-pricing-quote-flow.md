# Feature: Customers Menu & Pricing Quote Flow

## Feature Description
This feature adds a complete customer management and pricing quote workflow to the Valargen application. Users will be able to view a list of customers, request pricing quotes for mortgage products through the UWM API integration, and view detailed pricing responses. The feature includes:

1. **Customers Menu** - A new navigation item in the application sidebar/navbar
2. **Customer List View** - A table displaying customer records with pagination support
3. **Get Quote Action** - Per-customer action to request pricing quotes for non-HELOC loan products
4. **Real-time Loading States** - Visual feedback during API calls with inline spinners
5. **Pricing Response Storage** - Persistent storage of quote responses in the database
6. **Best Price Display** - Clickable links showing the best available price
7. **Pricing Details Modal** - Popup displaying comprehensive pricing information including full JSON response

This feature enables loan officers to efficiently manage customer relationships and obtain real-time pricing quotes from UWM's instant price quote API.

## User Story
As a loan officer
I want to view my customers and request instant pricing quotes for mortgage products
So that I can quickly provide accurate pricing information to customers and close more loans

## Problem Statement
Loan officers currently lack a way to manage customer information and obtain real-time pricing quotes within the Valargen application. They need to manually track customers and use external tools to get pricing information, which creates friction in the sales process and reduces efficiency. The application needs an integrated solution that combines customer management with instant pricing capabilities using the UWM API.

## Solution Statement
We will implement a comprehensive customer management and pricing quote feature that:

1. **Adds a dedicated Customers section** accessible from the main navigation, providing a centralized location for customer management
2. **Displays customers in a sortable, searchable table** with clear visibility of customer details and available actions
3. **Integrates with the UWM Instant Price Quote API** to fetch real-time pricing for non-HELOC loan products without exposing PHI
4. **Provides inline loading feedback** using spinners to indicate when quote requests are in progress
5. **Persists pricing responses** in the database linked to customers and users for future reference
6. **Displays the best available price** as a clickable element that opens a detailed modal
7. **Shows comprehensive pricing details** in a user-friendly modal including both the best price and complete JSON response

The solution follows the existing application patterns: Vue 3 frontend with reusable UI components, FastAPI backend with service layer architecture, PostgreSQL for data persistence, and proper multi-tenancy scoping.

## Relevant Files

### Backend Files (Existing)
- `app/server/main.py` - FastAPI application entry point where we'll register the new customers router
- `app/server/database.py` - Database session management and async connection handling
- `app/server/models/__init__.py` - Model registry where we'll add Customer and PricingQuote models
- `app/server/routers/__init__.py` - Router registry where we'll export the customers router
- `app/server/routers/users.py` - Reference example for router structure, authentication, and tenant scoping
- `app/server/routers/auth.py` - Reference for error handling patterns
- `app/server/schemas/user.py` - Reference example for Pydantic schema structure with nested models
- `app/server/services/oauth_service.py` - Reference example for external API integration using httpx
- `app/server/services/user_service.py` - Reference example for service layer patterns and database queries
- `app/server/config.py` - Application configuration where we'll add UWM API settings

### Frontend Files (Existing)
- `app/client/src/App.vue` - Root application component
- `app/client/src/router/index.js` - Vue Router configuration where we'll add the /customers route
- `app/client/src/components/AppNavbar.vue` - Navigation bar where we'll add the Customers menu item
- `app/client/src/views/DashboardView.vue` - Reference example for authenticated views and layout
- `app/client/src/views/ProfileView.vue` - Reference example for data fetching patterns
- `app/client/src/components/ui/BaseButton.vue` - Reusable button component with loading state support
- `app/client/src/components/ui/BaseCard.vue` - Reusable card component for layout
- `app/client/src/components/ui/BaseAlert.vue` - Reusable alert component for error messages
- `app/client/src/services/api.js` - Axios instance configuration with authentication interceptors
- `app/client/src/services/userService.js` - Reference example for service layer on frontend
- `app/client/src/stores/auth.js` - Auth store for current user access

### Documentation Files
- `README.md` - Project overview, architecture, and development setup
- `.claude/commands/conditional_docs.md` - Conditional documentation requirements
- `.claude/commands/test_e2e.md` - E2E test runner documentation
- `.claude/commands/e2e/test_basic_query.md` - Example E2E test structure
- `.claude/commands/e2e/test_user_login.md` - Example E2E test for authenticated flows

### New Files

#### Backend Models
- `app/server/models/customer.py` - Customer model with tenant scoping
- `app/server/models/pricing_quote.py` - PricingQuote model for storing quote responses

#### Backend Schemas
- `app/server/schemas/customer.py` - Customer Pydantic schemas (Create, Update, Response)
- `app/server/schemas/pricing_quote.py` - PricingQuote Pydantic schemas (Request, Response)

#### Backend Services
- `app/server/services/customer_service.py` - Customer business logic (CRUD operations)
- `app/server/services/pricing_service.py` - UWM API integration for instant price quotes

#### Backend Routers
- `app/server/routers/customers.py` - Customer endpoints (list, get, create, update)
- `app/server/routers/pricing.py` - Pricing endpoints (get quote)

#### Frontend Views
- `app/client/src/views/CustomersView.vue` - Main customers list view with table and quote actions

#### Frontend Components
- `app/client/src/components/CustomerTable.vue` - Table component displaying customers with inline actions
- `app/client/src/components/PricingModal.vue` - Modal component showing pricing details

#### Frontend Services
- `app/client/src/services/customerService.js` - Customer API calls
- `app/client/src/services/pricingService.js` - Pricing API calls

#### Database Migrations
- `app/server/alembic/versions/002_add_customers_table.py` - Migration for customers table
- `app/server/alembic/versions/003_add_pricing_quotes_table.py` - Migration for pricing_quotes table

#### Seed Data
- `app/server/scripts/seed_customers.py` - Script to create 15 sample customer records

#### E2E Tests
- `.claude/commands/e2e/test_customers_pricing_flow.md` - E2E test for the complete feature

## Implementation Plan

### Phase 1: Foundation
**Goal:** Set up the database schema, models, and seed data for the customers and pricing quotes feature.

1. Create the Customer model with proper multi-tenancy support (tenant_id foreign key)
2. Create the PricingQuote model to store quote responses linked to customers and users
3. Register both models in the models/__init__.py registry
4. Create Alembic migrations for both tables
5. Run migrations to update the database schema
6. Create a seed script to generate 15 sample customer records for each tenant
7. Run the seed script to populate test data

**Why this order:** Database schema must exist before any backend services or frontend can interact with customer data. Seed data is needed for immediate testing and demonstration.

### Phase 2: Core Implementation
**Goal:** Build the backend API services and endpoints for customer management and pricing integration.

1. Create Pydantic schemas for Customer (CustomerBase, CustomerCreate, CustomerUpdate, CustomerResponse, CustomerList)
2. Create Pydantic schemas for PricingQuote (PricingQuoteRequest, PricingQuoteResponse)
3. Implement CustomerService with tenant-scoped CRUD operations
4. Add UWM API configuration to config.py (API URL, API key, timeout settings)
5. Implement PricingService with UWM API integration using httpx (similar to oauth_service.py)
6. Create customers router with authenticated endpoints (list, get, create, update)
7. Create pricing router with authenticated quote endpoint
8. Register both routers in routers/__init__.py
9. Include both routers in main.py with /api prefix
10. Test all endpoints using FastAPI's /docs interface

**Why this order:** Schemas define the data contracts. Services implement business logic. Routers expose HTTP endpoints. This follows the layered architecture pattern used throughout the application.

### Phase 3: Integration
**Goal:** Build the frontend UI components and integrate with backend APIs to provide the complete user experience.

1. Create customerService.js with API methods (listCustomers, getCustomer, createCustomer, updateCustomer)
2. Create pricingService.js with API methods (getQuote)
3. Create PricingModal.vue component with slots for best price header and JSON display
4. Create CustomerTable.vue component with loading states, quote buttons, and price display
5. Create CustomersView.vue as the main page integrating the table component
6. Add /customers route to router/index.js with requiresAuth meta
7. Add Customers navigation link to AppNavbar.vue with appropriate icon
8. Test the complete flow: navigation → customer list → get quote → view modal
9. Create E2E test specification in .claude/commands/e2e/test_customers_pricing_flow.md
10. Run E2E test to validate the feature end-to-end

**Why this order:** Service layer first for API communication. Components built from smallest (modal) to largest (view). Router and navigation added last for integration. E2E test validates everything works together.

## Step by Step Tasks
IMPORTANT: Execute every step in order, top to bottom.

### 1. Create Customer Database Model
- Create `app/server/models/customer.py` with Customer model
- Fields: id (PK), tenant_id (FK to tenants), name, email, phone, company_name, timestamps
- Use SQLAlchemy 2.0 Mapped types following existing patterns
- Include proper cascade relationships and indexes
- Add __repr__ method for debugging

### 2. Create PricingQuote Database Model
- Create `app/server/models/pricing_quote.py` with PricingQuote model
- Fields: id (PK), customer_id (FK to customers), user_id (FK to users), tenant_id (FK to tenants), loan_type, best_price, full_response (JSONB), timestamps
- Link to customer, user, and tenant with proper cascade rules
- Use JSONB column type for full_response to store API response

### 3. Register Models
- Add Customer and PricingQuote imports to `app/server/models/__init__.py`
- Add both to __all__ list for proper module exposure

### 4. Create Database Migrations
- Run `cd app/server && alembic revision --autogenerate -m "Add customers table"`
- Run `cd app/server && alembic revision --autogenerate -m "Add pricing_quotes table"`
- Review generated migrations for correctness
- Run `cd app/server && alembic upgrade head` to apply migrations

### 5. Create Customer Seed Script
- Create `app/server/scripts/seed_customers.py`
- Generate 15 diverse sample customers with realistic names, emails, phone numbers, and company names
- Use faker library if available, otherwise hardcode realistic data
- Script should be idempotent and support multiple tenants
- Include proper async/await patterns matching existing scripts

### 6. Run Customer Seed Script
- Execute `cd app/server && uv run python scripts/seed_customers.py`
- Verify 15 customers created in database
- Check that customers are properly associated with test tenant

### 7. Create Customer Pydantic Schemas
- Create `app/server/schemas/customer.py`
- Define CustomerBase with common fields (name, email, phone, company_name)
- Define CustomerCreate extending CustomerBase
- Define CustomerUpdate with all optional fields
- Define CustomerResponse extending CustomerBase with id, tenant_id, timestamps
- Use proper Pydantic v2 patterns with Field validators and model_config

### 8. Create PricingQuote Pydantic Schemas
- Create `app/server/schemas/pricing_quote.py`
- Define PricingQuoteRequest with required fields per UWM API (loan_type, loan_amount, property_value, credit_score, etc.)
- Define PricingQuoteResponse with best_price, rate, apr, monthly_payment, full_response
- Use proper field validation and descriptions
- Add example data in model_config for API documentation

### 9. Implement CustomerService
- Create `app/server/services/customer_service.py`
- Implement create_customer(data, tenant_id, db) method
- Implement get_customer(customer_id, tenant_id, db) method with tenant scoping
- Implement list_customers(tenant_id, db) method with pagination support
- Implement update_customer(customer_id, data, tenant_id, db) method
- Include proper error handling and None checks
- Use async/await with AsyncSession
- Create singleton instance: customer_service = CustomerService()

### 10. Add UWM API Configuration
- Add UWM API settings to `app/server/config.py`
- Fields: uwm_api_url, uwm_api_key, uwm_api_timeout (with defaults)
- Use Field with env variable names (UWM_API_URL, UWM_API_KEY, UWM_API_TIMEOUT)
- Add validation and description strings
- Note: Since resource/uwm-instant-price-quote-api-reference.md doesn't exist, use placeholder URL and document that real API URL should be configured in .env

### 11. Implement PricingService with UWM API Integration
- Create `app/server/services/pricing_service.py`
- Implement get_instant_price_quote(request_data, customer_id, user_id, tenant_id, db) method
- Use httpx.AsyncClient() for API calls (follow oauth_service.py pattern)
- Build request payload according to UWM API requirements (non-HELOC, no PHI)
- Parse response and extract best price
- Save PricingQuote record to database with full response in JSONB
- Return formatted response with best price and quote ID
- Include proper error handling for API failures, timeouts, and invalid responses
- Add logging for debugging
- Create singleton instance: pricing_service = PricingService()
- NOTE: Since the API reference doc is missing, implement with reasonable assumptions for a mortgage pricing API

### 12. Create Customers Router
- Create `app/server/routers/customers.py`
- Define router with prefix="/customers" and tags=["customers"]
- Implement POST / endpoint to create customer (requires auth)
- Implement GET / endpoint to list customers for current tenant (requires auth)
- Implement GET /{customer_id} endpoint to get single customer (requires auth, tenant-scoped)
- Implement PATCH /{customer_id} endpoint to update customer (requires auth, tenant-scoped)
- Use Depends(get_current_user) for authentication
- Use Depends(get_db) for database sessions
- Return appropriate HTTP status codes (200, 201, 404, etc.)
- Include proper error handling with HTTPException

### 13. Create Pricing Router
- Create `app/server/routers/pricing.py`
- Define router with prefix="/pricing" and tags=["pricing"]
- Implement POST /quote endpoint to request pricing quote (requires auth)
- Accept customer_id and pricing request data in body
- Validate customer exists and belongs to user's tenant
- Call pricing_service.get_instant_price_quote()
- Return PricingQuoteResponse with best price and quote details
- Include proper error handling for API failures

### 14. Register Routers
- Add customers_router and pricing_router imports to `app/server/routers/__init__.py`
- Add both to __all__ list

### 15. Include Routers in Main Application
- Import customers_router and pricing_router in `app/server/main.py`
- Add app.include_router(customers_router, prefix="/api")
- Add app.include_router(pricing_router, prefix="/api")

### 16. Test Backend Endpoints Manually
- Start backend server: `cd app/server && uv run uvicorn main:app --reload`
- Open http://localhost:8000/docs
- Test POST /api/auth/login to get access token
- Test GET /api/customers to list customers
- Test POST /api/pricing/quote with sample customer ID and pricing data
- Verify responses match expected schemas
- Check database to confirm pricing quotes are saved

### 17. Create Customer Service on Frontend
- Create `app/client/src/services/customerService.js`
- Import api from './api.js'
- Implement listCustomers() - GET /api/customers
- Implement getCustomer(id) - GET /api/customers/:id
- Implement createCustomer(data) - POST /api/customers
- Implement updateCustomer(id, data) - PATCH /api/customers/:id
- Include proper error handling and response data extraction
- Follow patterns from userService.js

### 18. Create Pricing Service on Frontend
- Create `app/client/src/services/pricingService.js`
- Import api from './api.js'
- Implement getQuote(customerId, quoteData) - POST /api/pricing/quote
- Include proper error handling
- Return formatted response with bestPrice and fullResponse

### 19. Create PricingModal Component
- Create `app/client/src/components/PricingModal.vue`
- Props: show (boolean), bestPrice (string), fullResponse (object), onClose (function)
- Use fixed overlay with centered modal (follow modal patterns from other applications)
- Header section: Display "Pricing Quote" title and best price prominently (large font, bold)
- Body section: Display formatted JSON using <pre> tag with proper styling
- Footer section: Close button using BaseButton component
- Include backdrop click and ESC key to close
- Use Tailwind CSS for styling matching application design
- Add smooth enter/leave transitions

### 20. Create CustomerTable Component
- Create `app/client/src/components/CustomerTable.vue`
- Props: customers (array), loading (boolean)
- Display table with columns: Name, Email, Phone, Company, Best Price, Actions
- Each row includes customer data
- Best Price column shows clickable link if quote exists, otherwise shows "—"
- Actions column has "Get Quote" button using BaseButton with loading state
- Emit events: @quote-requested(customer), @price-clicked(customer)
- Include loading spinner overlay when loading prop is true
- Use responsive table with proper Tailwind styling
- Handle empty state with friendly message

### 21. Create CustomersView Component
- Create `app/client/src/views/CustomersView.vue`
- Import customerService, pricingService, CustomerTable, PricingModal, AppNavbar, BaseCard, BaseAlert
- Fetch customers list on component mount using customerService.listCustomers()
- Store customers in reactive ref
- Implement handleQuoteRequest(customer) method that calls pricingService.getQuote()
- Show inline loading state in specific table row during quote request
- Update customer's best price after successful quote
- Implement handlePriceClick(customer) that opens PricingModal with quote details
- Include error handling with BaseAlert for API failures
- Use AppNavbar and BaseCard for consistent layout
- Add page header "Customers" with count

### 22. Add Customers Route to Router
- Edit `app/client/src/router/index.js`
- Add new route object:
  - path: '/customers'
  - name: 'Customers'
  - component: lazy-loaded CustomersView
  - meta: { requiresAuth: true }
- Place after /profile route for logical grouping

### 23. Add Customers Link to Navigation
- Edit `app/client/src/components/AppNavbar.vue`
- Add new router-link for Customers between Dashboard and Profile links
- Use appropriate icon (users icon or customers icon)
- Match existing styling and hover effects
- Ensure icon and text sizing is consistent

### 24. Test Frontend Integration Manually
- Start backend: `cd app/server && uv run uvicorn main:app --reload`
- Start frontend: `cd app/client && bun run dev`
- Login at http://localhost:5173/login
- Click Customers in navigation
- Verify customer table loads with 15 records
- Click "Get Quote" button on first customer
- Verify spinner shows in row during request
- Verify best price link appears after quote completes
- Click best price link
- Verify modal opens with pricing details
- Verify modal close functionality works
- Test error scenarios by stopping backend

### 25. Create E2E Test Specification
- Create `.claude/commands/e2e/test_customers_pricing_flow.md`
- Follow structure from test_user_login.md
- Include User Story section
- Define Prerequisites (logged in user, backend running, seeded customers)
- List Test Steps:
  1. Navigate to /customers page
  2. Verify table loads with at least 10 customer records
  3. Take screenshot: customers_list_loaded.png
  4. Verify table columns: Name, Email, Phone, Company, Best Price, Actions
  5. Click "Get Quote" button on first customer row
  6. Verify loading spinner appears in row
  7. Take screenshot: quote_loading.png
  8. Wait for quote response (max 10 seconds)
  9. Verify loading spinner disappears
  10. Verify best price link appears in Best Price column
  11. Take screenshot: quote_completed.png
  12. Click best price link
  13. Verify modal opens
  14. Verify modal header shows "Pricing Quote"
  15. Verify best price is displayed prominently at top
  16. Take screenshot: pricing_modal_opened.png
  17. Verify full JSON response is displayed at bottom
  18. Scroll modal to view complete JSON
  19. Take screenshot: pricing_modal_json.png
  20. Click close button or backdrop
  21. Verify modal closes
  22. Take screenshot: modal_closed.png
- Define Success Criteria (all verifications pass, 6 screenshots captured)
- Document Expected API Calls (GET /api/customers, POST /api/pricing/quote)

### 26. Run All Validation Commands
- Execute every validation command listed in the Validation Commands section below
- Verify zero errors in server tests
- Verify zero errors in frontend TypeScript compilation
- Verify zero errors in frontend build
- Execute the E2E test and verify it passes with all screenshots captured
- Fix any issues discovered during validation

## Testing Strategy

### Unit Tests

**Backend Unit Tests:**
- `tests/test_customer_service.py` - Test customer CRUD operations
  - test_create_customer_success
  - test_create_customer_duplicate_email_allowed (different from user emails)
  - test_get_customer_by_id_success
  - test_get_customer_by_id_not_found
  - test_get_customer_wrong_tenant (security test)
  - test_list_customers_for_tenant
  - test_list_customers_empty
  - test_update_customer_success
  - test_update_customer_not_found

- `tests/test_pricing_service.py` - Test pricing API integration
  - test_get_instant_price_quote_success (with mocked httpx response)
  - test_get_instant_price_quote_api_error
  - test_get_instant_price_quote_timeout
  - test_get_instant_price_quote_saves_to_db
  - test_pricing_request_no_phi (verify no sensitive data in request)

- `tests/test_customers_router.py` - Test customer endpoints
  - test_list_customers_authenticated
  - test_list_customers_unauthenticated (should return 401)
  - test_get_customer_authenticated
  - test_get_customer_wrong_tenant (should return 404)
  - test_create_customer_authenticated
  - test_update_customer_authenticated

- `tests/test_pricing_router.py` - Test pricing endpoints
  - test_request_quote_authenticated
  - test_request_quote_invalid_customer
  - test_request_quote_customer_wrong_tenant (security test)

**Frontend Unit Tests (optional, if time permits):**
- Tests for customerService.js methods
- Tests for pricingService.js methods
- Component tests for PricingModal (props, events, close behavior)
- Component tests for CustomerTable (rendering, events)

### Edge Cases

1. **Multi-tenancy Security**
   - User from Tenant A cannot access customers from Tenant B
   - User from Tenant A cannot request quotes for customers in Tenant B
   - All queries properly filter by tenant_id

2. **API Integration Failures**
   - UWM API returns 500 error - should show user-friendly error message
   - UWM API times out - should show timeout error and not leave UI in loading state
   - UWM API returns malformed JSON - should handle gracefully
   - Network connectivity issues - should retry with exponential backoff (optional)

3. **Data Validation**
   - Empty customer list - should show "No customers found" message
   - Invalid customer ID in quote request - should return 404
   - Missing required fields in quote request - should return 400 with validation errors
   - Best price link only appears after successful quote - not for failed quotes

4. **UI/UX Edge Cases**
   - Multiple simultaneous quote requests - each row tracks its own loading state
   - Modal opened while quote request in progress - modal should not interfere
   - Rapid clicking of "Get Quote" button - should debounce or disable during request
   - Very long customer names or emails - should truncate with ellipsis in table
   - Large JSON responses - modal should scroll properly
   - Mobile responsive - table should scroll horizontally on small screens

5. **Authentication Edge Cases**
   - Token expires during quote request - should refresh token and retry
   - User logs out while viewing customers page - should redirect to login
   - Accessing /customers without authentication - should redirect to login

6. **Performance**
   - Large number of customers (100+) - consider pagination (future enhancement)
   - Large JSON responses (>10KB) - ensure modal renders without lag

## Acceptance Criteria

1. **Navigation & Access**
   - [ ] Customers menu item appears in navigation bar for authenticated users
   - [ ] Clicking Customers navigates to /customers route
   - [ ] Unauthenticated users are redirected to login when accessing /customers

2. **Customer List Display**
   - [ ] Customer table displays with columns: Name, Email, Phone, Company, Best Price, Actions
   - [ ] At least 10 customer records are visible after seeding
   - [ ] Table is responsive and scrolls horizontally on mobile devices
   - [ ] Empty state shows friendly message when no customers exist

3. **Get Quote Functionality**
   - [ ] Each customer row has a "Get Quote" button
   - [ ] Clicking "Get Quote" triggers a pricing request to UWM API
   - [ ] API request includes only required fields with no PHI
   - [ ] Request is properly scoped to current user's tenant

4. **Loading States**
   - [ ] Spinner appears in the specific table row during quote request
   - [ ] Loading state is confined to the active row, other rows remain interactive
   - [ ] Loading state clears after response (success or failure)

5. **Pricing Response Storage**
   - [ ] Successful quote responses are saved to pricing_quotes table
   - [ ] Saved records include customer_id, user_id, tenant_id, best_price, full_response
   - [ ] Full API response is stored in JSONB column

6. **Best Price Display**
   - [ ] Best Price column shows "—" for customers without quotes
   - [ ] Best Price column shows clickable link after successful quote
   - [ ] Link displays the actual best price value (e.g., "$350,000")
   - [ ] Link has hover effect indicating it's clickable

7. **Pricing Modal**
   - [ ] Clicking best price link opens modal
   - [ ] Modal displays "Pricing Quote" title
   - [ ] Best price is shown prominently at the top of modal
   - [ ] Full JSON response is displayed in readable format at bottom
   - [ ] JSON is syntax highlighted or formatted with proper indentation
   - [ ] Modal has close button that works
   - [ ] Clicking backdrop closes modal
   - [ ] Pressing ESC key closes modal
   - [ ] Modal scrolls properly for large JSON responses

8. **Error Handling**
   - [ ] API errors show user-friendly error messages using BaseAlert
   - [ ] Timeout errors are handled gracefully
   - [ ] Network errors don't leave UI in broken state
   - [ ] Validation errors display specific field errors

9. **Security & Multi-tenancy**
   - [ ] All customer queries are scoped to current user's tenant_id
   - [ ] Users cannot access customers from other tenants
   - [ ] Users cannot request quotes for customers in other tenants
   - [ ] All endpoints require authentication

10. **E2E Test**
    - [ ] E2E test executes successfully from start to finish
    - [ ] All 6 required screenshots are captured
    - [ ] Test validates complete user workflow
    - [ ] Test verifies API integration works end-to-end

## Validation Commands
Execute every command to validate the feature works correctly with zero regressions.

- Read `.claude/commands/test_e2e.md`, then read and execute `.claude/commands/e2e/test_customers_pricing_flow.md` to validate the complete feature workflow
- `cd app/server && uv run pytest` - Run server tests to validate the feature works with zero regressions
- `cd app/client && bun tsc --noEmit` - Run frontend TypeScript checks to validate no type errors
- `cd app/client && bun run build` - Run frontend build to validate the feature builds successfully

## Notes

### UWM API Reference Missing
The feature specification references `resource/uwm-instant-price-quote-api-reference.md` which does not exist in the codebase. The implementation will make reasonable assumptions for a mortgage pricing API based on industry standards:

**Assumed Request Fields:**
- loan_amount (required)
- property_value (required)
- credit_score (required)
- loan_type (required, non-HELOC: conventional, FHA, VA, USDA)
- loan_purpose (purchase, refinance, cash-out)
- property_type (single-family, condo, townhouse)
- occupancy (primary, secondary, investment)
- state (property location)

**Assumed Response Structure:**
```json
{
  "best_price": "$350,000",
  "rate": "6.25%",
  "apr": "6.35%",
  "monthly_payment": "$2,154.32",
  "loan_id": "abc123",
  "pricing_tiers": [...],
  "lock_days": 30,
  "fees": {...}
}
```

**API Configuration:**
The real UWM API URL and API key should be configured via environment variables:
```env
UWM_API_URL=https://api.uwm.com/v1/pricing/instant-quote
UWM_API_KEY=your_api_key_here
UWM_API_TIMEOUT=10
```

### Future Enhancements
While not part of the current scope, consider these enhancements for future iterations:

1. **Pagination** - For tenants with hundreds of customers, implement cursor-based or offset pagination
2. **Search & Filtering** - Add search by name/email and filters by company
3. **Sorting** - Allow sorting by any column (name, email, recent quotes)
4. **Quote History** - Show all previous quotes for a customer, not just the latest
5. **Edit Customers** - Add ability to update customer information
6. **Delete Customers** - Soft delete with confirmation modal
7. **Export** - CSV export of customer list and pricing data
8. **Real-time Updates** - WebSocket notifications when quotes complete
9. **Quote Parameters** - Allow customizing loan parameters before requesting quote
10. **Comparison View** - Compare multiple quotes side-by-side

### Dependencies to Add
If the following libraries are not already in the project, add them:

**Backend:**
```bash
cd app/server
uv add httpx  # For async HTTP requests (likely already present)
uv add faker  # For generating realistic seed data
```

**Frontend:**
No new dependencies required - using existing Vue 3, Axios, Tailwind CSS

### Performance Considerations
- The current implementation loads all customers at once. This is acceptable for the MVP with 15 sample records
- For production with many customers, implement pagination on both backend and frontend
- Consider adding database indexes on frequently queried fields (email, company_name, tenant_id)
- UWM API requests may take several seconds - ensure timeout is appropriately configured
- Consider caching recent quotes to reduce duplicate API calls

### Code Quality Standards
- Follow existing patterns for async/await, error handling, and component structure
- Use TypeScript-style JSDoc comments for better IDE support
- Maintain consistent naming conventions (camelCase for JS, snake_case for Python)
- Include docstrings for all Python functions
- Use Tailwind utility classes, avoid custom CSS when possible
- Keep components focused and single-purpose
- Extract magic numbers and strings to constants

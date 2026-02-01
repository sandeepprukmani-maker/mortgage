# Feature: User Authentication & Session Management (Email + Google OAuth)

## Feature Description
This feature implements a comprehensive authentication and session management system for the Valargen mortgage automation platform. It provides two authentication methods: traditional email/password authentication with Argon2 password hashing, and OAuth2 integration with Google for seamless single sign-on. The system uses JWT tokens for stateless authentication with refresh token rotation for enhanced security. Users can register, login, manage passwords, and access their profile information based on their assigned roles and tenant subscriptions. The implementation follows security best practices including rate limiting, secure password requirements, and protection against common vulnerabilities like email enumeration.

## User Story
As a **Loan Officer or Admin**
I want to securely authenticate into the Valargen platform using either my email/password or my Google account
So that I can access my permitted modules and manage mortgage automation workflows with confidence that my data is protected

## Problem Statement
The Valargen platform currently lacks a user authentication system, preventing secure access control and user management. Without authentication, the system cannot:
- Identify and authorize users accessing sensitive mortgage data
- Differentiate between loan officers, admins, and other roles
- Protect against unauthorized access to automation workflows
- Track user activity and maintain audit trails
- Support multi-tenant architecture with subscription-based access control
- Provide modern OAuth authentication options users expect

## Solution Statement
Implement a robust JWT-based authentication system with dual authentication methods (local email/password and Google OAuth). The solution uses Argon2 for secure password hashing, implements refresh token rotation for enhanced security, and includes rate limiting to prevent brute force attacks. The backend uses FastAPI with SQLAlchemy for database operations and Alembic for migrations. The frontend Vue 3 application will provide login/registration forms and handle token management. The system integrates with a multi-tenant architecture supporting role-based access control (RBAC) and subscription-based feature access.

## Relevant Files
Use these files to implement the feature:

### Backend Core Files
- **app/server/main.py** - FastAPI application entry point, will mount auth router and configure middleware
- **app/server/database.py** - Database connection management, will be extended with SQLAlchemy session management
- **app/server/.env.sample** - Environment variables template, needs JWT and OAuth secrets
- **app/server/pyproject.toml** - Python dependencies, will add auth-related packages

### Backend Test Files
- **app/server/tests/test_health.py** - Existing test pattern, will follow for auth tests
- **app/server/tests/__init__.py** - Test package initialization

### Frontend Files
- **app/client/src/App.vue** - Main Vue component, will be replaced with auth-aware routing
- **app/client/src/main.js** - Vue app initialization
- **app/client/package.json** - Frontend dependencies, will add auth and routing packages

### Infrastructure Files
- **docker-compose.yml** - Docker services configuration, already includes PostgreSQL and Redis
- **README.md** - Project documentation, will be updated with auth setup instructions

### Documentation Reference Files
- **.claude/commands/test_e2e.md** - E2E test runner pattern to follow
- **.claude/commands/e2e/test_basic_query.md** - Example E2E test structure
- **.claude/commands/conditional_docs.md** - Conditional documentation guide

### New Files

#### Backend - Database Models
- **app/server/models/__init__.py** - Models package initialization
- **app/server/models/user.py** - User model with authentication fields
- **app/server/models/tenant.py** - Tenant/organization model for multi-tenancy
- **app/server/models/role.py** - Role model for RBAC
- **app/server/models/permission.py** - Permission model for granular access control
- **app/server/models/refresh_token.py** - Refresh token model for token management
- **app/server/models/password_reset.py** - Password reset token model

#### Backend - Database Migrations
- **app/server/alembic.ini** - Alembic configuration
- **app/server/alembic/env.py** - Alembic environment configuration
- **app/server/alembic/versions/001_initial_auth_schema.py** - Initial database schema migration

#### Backend - Schemas (Pydantic)
- **app/server/schemas/__init__.py** - Schemas package initialization
- **app/server/schemas/auth.py** - Authentication request/response schemas
- **app/server/schemas/user.py** - User-related schemas
- **app/server/schemas/token.py** - JWT token schemas

#### Backend - Services/Business Logic
- **app/server/services/__init__.py** - Services package initialization
- **app/server/services/auth_service.py** - Authentication business logic
- **app/server/services/user_service.py** - User management business logic
- **app/server/services/token_service.py** - JWT token generation/validation
- **app/server/services/password_service.py** - Password hashing/validation with Argon2
- **app/server/services/oauth_service.py** - Google OAuth integration
- **app/server/services/rate_limit_service.py** - Rate limiting logic using Redis

#### Backend - API Routes
- **app/server/routers/__init__.py** - Routers package initialization
- **app/server/routers/auth.py** - Authentication endpoints (register, login, logout, etc.)
- **app/server/routers/users.py** - User profile endpoints

#### Backend - Dependencies/Middleware
- **app/server/dependencies/auth.py** - FastAPI dependencies for authentication (get_current_user, require_role, etc.)
- **app/server/middleware/auth.py** - JWT authentication middleware

#### Backend - Utilities
- **app/server/utils/__init__.py** - Utilities package initialization
- **app/server/utils/security.py** - Security utility functions
- **app/server/utils/validators.py** - Input validation utilities

#### Backend - Configuration
- **app/server/config.py** - Application configuration management using Pydantic settings

#### Backend - Tests
- **app/server/tests/conftest.py** - Pytest fixtures and configuration
- **app/server/tests/test_auth.py** - Authentication endpoint tests
- **app/server/tests/test_user_service.py** - User service tests
- **app/server/tests/test_password_service.py** - Password service tests
- **app/server/tests/test_oauth_service.py** - OAuth service tests
- **app/server/tests/test_token_service.py** - Token service tests
- **app/server/tests/test_rate_limiting.py** - Rate limiting tests

#### Frontend - Components
- **app/client/src/components/LoginForm.vue** - Email/password login form
- **app/client/src/components/RegisterForm.vue** - User registration form
- **app/client/src/components/ForgotPasswordForm.vue** - Forgot password form
- **app/client/src/components/ResetPasswordForm.vue** - Reset password form
- **app/client/src/components/GoogleLoginButton.vue** - Google OAuth login button
- **app/client/src/components/UserProfile.vue** - User profile display component
- **app/client/src/components/ProtectedRoute.vue** - Route guard component

#### Frontend - Views
- **app/client/src/views/LoginView.vue** - Login page view
- **app/client/src/views/RegisterView.vue** - Registration page view
- **app/client/src/views/ForgotPasswordView.vue** - Forgot password page view
- **app/client/src/views/ResetPasswordView.vue** - Reset password page view
- **app/client/src/views/DashboardView.vue** - Authenticated dashboard view
- **app/client/src/views/ProfileView.vue** - User profile page view

#### Frontend - Services
- **app/client/src/services/api.js** - Axios API client with token management
- **app/client/src/services/authService.js** - Authentication API calls
- **app/client/src/services/userService.js** - User API calls

#### Frontend - Store (State Management)
- **app/client/src/stores/auth.js** - Pinia auth store for state management
- **app/client/src/stores/user.js** - Pinia user store

#### Frontend - Router
- **app/client/src/router/index.js** - Vue Router configuration with auth guards

#### Frontend - Composables
- **app/client/src/composables/useAuth.js** - Auth composable for Vue components
- **app/client/src/composables/useGoogleAuth.js** - Google OAuth composable

#### E2E Tests
- **.claude/commands/e2e/test_user_registration.md** - E2E test for user registration flow
- **.claude/commands/e2e/test_user_login.md** - E2E test for login flow
- **.claude/commands/e2e/test_google_oauth.md** - E2E test for Google OAuth flow
- **.claude/commands/e2e/test_password_reset.md** - E2E test for password reset flow

## Implementation Plan

### Phase 1: Foundation (Database & Core Infrastructure)
Set up the foundational database schema, models, and core authentication infrastructure before implementing business logic. This includes:
- Installing required Python packages (SQLAlchemy, Alembic, passlib[argon2], python-jose, authlib, redis)
- Installing required Node packages (vue-router, pinia, axios)
- Creating database models for users, tenants, roles, permissions, and tokens
- Setting up Alembic for database migrations
- Creating initial migration script for authentication schema
- Configuring application settings and environment variables
- Setting up Redis connection for rate limiting and session management

### Phase 2: Core Implementation (Authentication Services & API)
Implement the core authentication functionality including password hashing, JWT token management, OAuth integration, and API endpoints. This includes:
- Implementing password service with Argon2 hashing and validation
- Implementing JWT token service with access/refresh token generation and validation
- Implementing rate limiting service using Redis
- Implementing Google OAuth service for authentication
- Creating authentication business logic (register, login, logout, password reset)
- Building FastAPI router endpoints for authentication operations
- Implementing authentication middleware and dependencies
- Creating Pydantic schemas for request/response validation
- Writing comprehensive unit tests for all services

### Phase 3: Integration (Frontend & E2E Testing)
Build the frontend user interface and integrate with backend APIs, then validate the complete system with E2E tests. This includes:
- Setting up Vue Router with authentication guards
- Setting up Pinia stores for state management
- Creating authentication forms (login, register, password reset)
- Implementing Google OAuth button and flow
- Building protected routes and user profile views
- Creating API service layer with token management
- Implementing token refresh logic and interceptors
- Creating E2E test specifications for all authentication flows
- Running E2E tests to validate end-to-end functionality
- Updating documentation with authentication setup instructions

## Step by Step Tasks

### 1. Install Backend Dependencies
- Add `sqlalchemy>=2.0.0` to pyproject.toml for ORM functionality
- Add `alembic>=1.13.0` for database migrations
- Add `passlib[argon2]>=1.7.4` for password hashing with Argon2
- Add `python-jose[cryptography]>=3.3.0` for JWT token handling
- Add `python-multipart>=0.0.6` for form data handling
- Add `authlib>=1.3.0` for Google OAuth integration
- Add `redis>=5.0.0` for rate limiting and caching
- Run `cd app/server && uv add sqlalchemy alembic passlib[argon2] python-jose[cryptography] python-multipart authlib redis` to install all packages

### 2. Install Frontend Dependencies
- Add `vue-router@4` for routing
- Add `pinia@2` for state management
- Add `axios@1` for HTTP requests
- Add `@vueuse/core@10` for Vue composition utilities
- Run `cd app/client && bun add vue-router pinia axios @vueuse/core` to install packages
- Run `cd app/client && bun add -D @types/node` for TypeScript type definitions

### 3. Create Backend Configuration Module
- Create `app/server/config.py` with Pydantic BaseSettings
- Define configuration for:
  - Database connection URL
  - JWT secret key and algorithm (HS256)
  - Access token expiry (15 minutes)
  - Refresh token expiry (7 days)
  - Google OAuth client ID and secret
  - Redis URL for rate limiting
  - Password validation rules
  - Rate limiting thresholds (5 attempts, 15 min lockout)
- Load configuration from environment variables with defaults
- Add validation for required settings

### 4. Update Environment Variables
- Update `app/server/.env.sample` with new variables:
  - `JWT_SECRET_KEY` (generate secure random key)
  - `JWT_ALGORITHM=HS256`
  - `ACCESS_TOKEN_EXPIRE_MINUTES=15`
  - `REFRESH_TOKEN_EXPIRE_DAYS=7`
  - `GOOGLE_CLIENT_ID` (from Google Cloud Console)
  - `GOOGLE_CLIENT_SECRET` (from Google Cloud Console)
  - `GOOGLE_REDIRECT_URI=http://localhost:8000/api/auth/google/callback`
  - `FRONTEND_URL=http://localhost:5173`
- Document OAuth setup instructions in comments

### 5. Extend Database Module
- Update `app/server/database.py` to use SQLAlchemy ORM
- Create SQLAlchemy engine with async support (asyncpg)
- Create async session maker
- Create declarative base class for models
- Implement `get_db()` dependency for FastAPI
- Keep existing `check_database_connection()` function
- Add database initialization function

### 6. Create Database Models
- Create `app/server/models/__init__.py` and export all models
- Create `app/server/models/tenant.py`:
  - Tenant model with id, company_name, plan (free/basic/premium), is_active, created_at, updated_at
  - Relationship to users
- Create `app/server/models/role.py`:
  - Role model with id, name (loan_officer/admin/super_admin), description
  - Relationship to users and permissions
- Create `app/server/models/permission.py`:
  - Permission model with id, name, description, module
  - Relationship to roles (many-to-many)
- Create `app/server/models/user.py`:
  - User model with id, email, password_hash (nullable), first_name, last_name
  - auth_provider (local/google), google_id (nullable), is_email_verified
  - tenant_id (foreign key), role_id (foreign key)
  - last_login_at, failed_login_attempts, locked_until, created_at, updated_at
  - Relationships to tenant, role, refresh_tokens, password_resets
- Create `app/server/models/refresh_token.py`:
  - RefreshToken model with id, token (UUID), user_id (foreign key)
  - expires_at, is_revoked, created_at
  - Relationship to user
- Create `app/server/models/password_reset.py`:
  - PasswordResetToken model with id, token (UUID), user_id (foreign key)
  - expires_at, is_used, created_at
  - Relationship to user

### 7. Setup Alembic for Migrations
- Create `app/server/alembic.ini` configuration file
- Create `app/server/alembic/` directory structure
- Create `app/server/alembic/env.py` with async support
- Configure Alembic to use SQLAlchemy metadata
- Set up migration file naming convention
- Initialize Alembic repository

### 8. Create Initial Database Migration
- Create `app/server/alembic/versions/001_initial_auth_schema.py`
- Define upgrade() function to create all tables:
  - tenants table
  - roles table
  - permissions table
  - role_permissions junction table
  - users table
  - refresh_tokens table
  - password_reset_tokens table
- Define downgrade() function to drop tables in reverse order
- Add indexes for performance (email, google_id, tokens)
- Add unique constraints (email, google_id)

### 9. Create Seed Data Script
- Create `app/server/scripts/seed_data.py` to populate initial data
- Seed default roles: loan_officer, admin, super_admin
- Seed default permissions based on module access
- Seed a default tenant for testing
- Seed an admin user for testing
- Make script idempotent (check before inserting)

### 10. Create Pydantic Schemas
- Create `app/server/schemas/__init__.py` and export schemas
- Create `app/server/schemas/token.py`:
  - TokenResponse (access_token, token_type, expires_in)
  - TokenRefreshRequest (refresh_token)
- Create `app/server/schemas/user.py`:
  - UserBase, UserCreate, UserUpdate, UserResponse, UserProfile
  - Include tenant and role information in response schemas
- Create `app/server/schemas/auth.py`:
  - RegisterRequest (email, password, first_name, last_name)
  - LoginRequest (email, password)
  - ForgotPasswordRequest (email)
  - ResetPasswordRequest (token, new_password)
  - GoogleCallbackRequest (code, state)
- Add validators for email format and password requirements

### 11. Create Password Service
- Create `app/server/services/__init__.py`
- Create `app/server/services/password_service.py`
- Implement `hash_password(password: str) -> str` using Argon2
- Implement `verify_password(plain: str, hashed: str) -> bool`
- Implement `validate_password_strength(password: str) -> bool`
  - Check minimum 8 characters
  - Check at least 1 uppercase letter
  - Check at least 1 number
  - Raise validation error if requirements not met
- Use passlib CryptContext with argon2 scheme

### 12. Create Token Service
- Create `app/server/services/token_service.py`
- Implement `create_access_token(user_id: int, email: str) -> str`
  - Generate JWT with user_id and email claims
  - Set expiry to 15 minutes
  - Use HS256 algorithm
- Implement `create_refresh_token(user_id: int) -> RefreshToken`
  - Generate UUID token
  - Store in database with 7-day expiry
  - Return token object
- Implement `verify_access_token(token: str) -> dict`
  - Decode JWT and validate signature
  - Check expiry
  - Return claims if valid, raise exception otherwise
- Implement `verify_refresh_token(token: str) -> RefreshToken`
  - Look up token in database
  - Check if revoked or expired
  - Return token object if valid
- Implement `revoke_refresh_token(token: str)`
  - Mark token as revoked in database

### 13. Create Rate Limiting Service
- Create `app/server/services/rate_limit_service.py`
- Implement Redis-based rate limiting
- Implement `check_rate_limit(identifier: str) -> tuple[bool, int]`
  - Use identifier (email or IP) as Redis key
  - Track failed login attempts
  - Return (is_locked, attempts_remaining)
- Implement `increment_failed_attempts(identifier: str)`
  - Increment counter in Redis
  - Set 15-minute expiry after 5th attempt
- Implement `reset_failed_attempts(identifier: str)`
  - Delete Redis key on successful login

### 14. Create OAuth Service
- Create `app/server/services/oauth_service.py`
- Implement `get_google_authorization_url() -> str`
  - Generate OAuth authorization URL
  - Include redirect URI and scopes (email, profile)
  - Return URL for frontend redirect
- Implement `exchange_code_for_token(code: str) -> dict`
  - Exchange authorization code for access token
  - Call Google token endpoint
  - Return token response
- Implement `get_google_user_info(access_token: str) -> dict`
  - Call Google userinfo endpoint
  - Extract email, given_name, family_name, picture
  - Return user data

### 15. Create User Service
- Create `app/server/services/user_service.py`
- Implement `create_user(data: UserCreate, tenant_id: int, role_id: int) -> User`
  - Validate email uniqueness
  - Hash password if provided
  - Create user record
  - Return user object
- Implement `get_user_by_email(email: str) -> User | None`
- Implement `get_user_by_id(user_id: int) -> User | None`
- Implement `get_user_by_google_id(google_id: str) -> User | None`
- Implement `update_last_login(user_id: int)`
  - Update last_login_at timestamp
  - Reset failed login attempts
- Implement `update_failed_login_attempts(user_id: int, increment: bool)`
- Implement `get_user_profile(user_id: int) -> dict`
  - Fetch user with tenant and role relationships
  - Include available modules based on subscription plan
  - Return comprehensive profile data

### 16. Create Authentication Service
- Create `app/server/services/auth_service.py`
- Implement `register_user(data: RegisterRequest) -> User`
  - Validate password strength
  - Check email uniqueness
  - Create default tenant if needed
  - Assign loan_officer role by default
  - Create user with auth_provider='local'
  - Return user (no auto-login)
- Implement `login_user(email: str, password: str) -> tuple[str, RefreshToken, User]`
  - Check rate limiting
  - Look up user by email
  - Verify auth_provider is 'local'
  - Verify password
  - Update last login timestamp
  - Reset failed attempts
  - Generate access and refresh tokens
  - Return (access_token, refresh_token, user)
  - Increment failed attempts on error
- Implement `login_with_google(code: str) -> tuple[str, RefreshToken, User]`
  - Exchange code for Google access token
  - Fetch Google user info
  - Check if user exists by email
  - If exists with auth_provider='local', raise error
  - If exists with auth_provider='google', login user
  - If not exists, auto-register new user
  - Generate access and refresh tokens
  - Return (access_token, refresh_token, user)
- Implement `logout_user(refresh_token: str)`
  - Revoke refresh token
- Implement `refresh_access_token(refresh_token: str) -> tuple[str, RefreshToken]`
  - Verify refresh token
  - Generate new access token
  - Rotate refresh token (revoke old, create new)
  - Return (new_access_token, new_refresh_token)
- Implement `request_password_reset(email: str)`
  - Look up user by email
  - Check auth_provider is 'local'
  - Generate UUID reset token with 1-hour expiry
  - Store token in database
  - Log reset URL to console (no email for MVP)
  - Always return success (prevent enumeration)
- Implement `reset_password(token: str, new_password: str)`
  - Look up reset token in database
  - Verify not expired and not used
  - Validate new password strength
  - Hash new password
  - Update user password
  - Mark token as used

### 17. Create Authentication Dependencies
- Create `app/server/dependencies/__init__.py`
- Create `app/server/dependencies/auth.py`
- Implement `get_current_user(token: str = Depends(oauth2_scheme)) -> User`
  - Extract token from Authorization header
  - Verify access token
  - Look up user by ID from token claims
  - Raise 401 if token invalid or user not found
  - Return user object
- Implement `require_role(allowed_roles: list[str])`
  - Dependency factory that checks user role
  - Raise 403 if user role not in allowed_roles
- Implement `get_optional_user(token: str | None) -> User | None`
  - Similar to get_current_user but returns None if no token

### 18. Create Authentication Router
- Create `app/server/routers/__init__.py`
- Create `app/server/routers/auth.py`
- Mount APIRouter with prefix `/auth` and tag `authentication`
- Implement `POST /auth/register`:
  - Accept RegisterRequest body
  - Call auth_service.register_user()
  - Return success message (no tokens)
  - Return 400 on validation errors
  - Return 409 if email already exists
- Implement `POST /auth/login`:
  - Accept LoginRequest body (email, password)
  - Call auth_service.login_user()
  - Set refresh token in HTTPOnly cookie
  - Return TokenResponse with access token
  - Return 401 on invalid credentials
  - Return 429 on rate limit exceeded
- Implement `POST /auth/logout`:
  - Extract refresh token from cookie
  - Call auth_service.logout_user()
  - Clear refresh token cookie
  - Return success message
- Implement `POST /auth/refresh`:
  - Extract refresh token from cookie
  - Call auth_service.refresh_access_token()
  - Set new refresh token in HTTPOnly cookie
  - Return TokenResponse with new access token
  - Return 401 if refresh token invalid
- Implement `GET /auth/google`:
  - Call oauth_service.get_google_authorization_url()
  - Return authorization URL for frontend redirect
- Implement `GET /auth/google/callback`:
  - Accept code query parameter
  - Call auth_service.login_with_google()
  - Set refresh token in HTTPOnly cookie
  - Redirect to frontend with access token in URL fragment
  - Return 400 on OAuth errors
- Implement `POST /auth/forgot-password`:
  - Accept ForgotPasswordRequest body
  - Call auth_service.request_password_reset()
  - Always return success message
- Implement `POST /auth/reset-password`:
  - Accept ResetPasswordRequest body
  - Call auth_service.reset_password()
  - Return success message
  - Return 400 on invalid/expired token

### 19. Create User Router
- Create `app/server/routers/users.py`
- Mount APIRouter with prefix `/users` and tag `users`
- Implement `GET /users/me`:
  - Require authentication with get_current_user dependency
  - Call user_service.get_user_profile()
  - Return UserProfile schema
  - Include tenant, role, permissions, available modules
- Implement `PATCH /users/me`:
  - Require authentication
  - Accept UserUpdate body (first_name, last_name)
  - Update user record
  - Return updated UserProfile

### 20. Update Main Application
- Update `app/server/main.py`
- Import and include auth router: `app.include_router(auth.router, prefix="/api")`
- Import and include users router: `app.include_router(users.router, prefix="/api")`
- Add CORS configuration to allow credentials
- Update allowed origins to include frontend URL
- Add startup event to initialize database (run migrations if needed)
- Keep existing health endpoint

### 21. Write Backend Unit Tests - Password Service
- Create `app/server/tests/conftest.py` with pytest fixtures:
  - Database session fixture
  - Test client fixture
  - Mock Redis fixture
  - Test user fixtures
- Create `app/server/tests/test_password_service.py`
- Test password hashing creates different hashes for same password
- Test password verification succeeds with correct password
- Test password verification fails with incorrect password
- Test password strength validation accepts valid passwords
- Test password strength validation rejects weak passwords (too short, no uppercase, no number)

### 22. Write Backend Unit Tests - Token Service
- Create `app/server/tests/test_token_service.py`
- Test access token creation includes correct claims
- Test access token verification succeeds with valid token
- Test access token verification fails with expired token
- Test access token verification fails with invalid signature
- Test refresh token creation stores in database
- Test refresh token verification succeeds with valid token
- Test refresh token verification fails with revoked token
- Test refresh token verification fails with expired token
- Test refresh token revocation marks token as revoked

### 23. Write Backend Unit Tests - Rate Limiting Service
- Create `app/server/tests/test_rate_limiting.py`
- Test rate limit allows requests under threshold
- Test rate limit blocks requests after threshold exceeded
- Test rate limit returns correct remaining attempts
- Test rate limit resets after successful login
- Test rate limit expires after lockout period

### 24. Write Backend Unit Tests - User Service
- Create `app/server/tests/test_user_service.py`
- Test create_user with local auth provider
- Test create_user with Google auth provider
- Test create_user fails with duplicate email
- Test get_user_by_email returns correct user
- Test get_user_by_email returns None for non-existent email
- Test get_user_by_google_id returns correct user
- Test update_last_login updates timestamp
- Test get_user_profile includes tenant and role data

### 25. Write Backend Unit Tests - Authentication Service
- Create `app/server/tests/test_auth.py`
- Test user registration creates user correctly
- Test user registration validates password strength
- Test user registration fails with duplicate email
- Test login succeeds with correct credentials
- Test login fails with incorrect password
- Test login fails when rate limit exceeded
- Test login fails for Google users trying to use password
- Test logout revokes refresh token
- Test token refresh returns new tokens
- Test token refresh fails with invalid token
- Test password reset request generates token
- Test password reset request always returns success
- Test password reset succeeds with valid token
- Test password reset fails with expired token
- Test password reset fails with used token

### 26. Write Backend Unit Tests - OAuth Service
- Create `app/server/tests/test_oauth_service.py`
- Test get_google_authorization_url returns valid URL
- Test exchange_code_for_token with mocked Google API
- Test get_google_user_info with mocked Google API
- Test OAuth error handling

### 27. Write Backend Integration Tests
- Create `app/server/tests/test_auth_endpoints.py`
- Test full registration flow (POST /auth/register)
- Test full login flow (POST /auth/login)
- Test logout flow (POST /auth/logout)
- Test token refresh flow (POST /auth/refresh)
- Test get current user (GET /users/me)
- Test protected endpoint without token returns 401
- Test protected endpoint with invalid token returns 401
- Test protected endpoint with valid token returns 200
- Test password reset request flow
- Test password reset flow
- Test rate limiting on login endpoint

### 28. Run Database Migration
- Run `cd app/server && uv run alembic upgrade head` to create tables
- Verify tables created in PostgreSQL
- Run seed data script to populate initial roles and permissions
- Verify seed data inserted correctly

### 29. Setup Vue Router
- Create `app/client/src/router/index.js`
- Configure Vue Router with routes:
  - `/` → Redirect to `/login` if not authenticated, `/dashboard` if authenticated
  - `/login` → LoginView (guest only)
  - `/register` → RegisterView (guest only)
  - `/forgot-password` → ForgotPasswordView (guest only)
  - `/reset-password/:token` → ResetPasswordView (guest only)
  - `/dashboard` → DashboardView (protected)
  - `/profile` → ProfileView (protected)
- Implement navigation guards:
  - `beforeEach` guard to check authentication
  - Redirect to login if not authenticated and accessing protected route
  - Redirect to dashboard if authenticated and accessing guest-only route
- Export router

### 30. Setup Pinia Stores
- Create `app/client/src/stores/auth.js`
- Define auth store with state:
  - `accessToken` (string | null)
  - `user` (object | null)
  - `isAuthenticated` (boolean computed)
- Define actions:
  - `setAuth(accessToken, user)` - Store token and user data
  - `clearAuth()` - Clear authentication state
  - `checkAuth()` - Check if user is authenticated (validate token)
- Persist accessToken to localStorage
- Create `app/client/src/stores/user.js`
- Define user store with state:
  - `profile` (object | null)
- Define actions:
  - `fetchProfile()` - Fetch user profile from API
  - `updateProfile(data)` - Update user profile

### 31. Create API Service Layer
- Create `app/client/src/services/api.js`
- Configure Axios instance with:
  - Base URL from environment variable (VITE_API_URL)
  - Credentials enabled (withCredentials: true)
  - Request interceptor to add Authorization header with access token
  - Response interceptor to handle 401 errors (attempt token refresh)
  - Implement token refresh logic in interceptor
  - Retry failed request after token refresh
- Export configured Axios instance

### 32. Create Auth Service Layer
- Create `app/client/src/services/authService.js`
- Implement API functions:
  - `register(email, password, firstName, lastName)` → POST /api/auth/register
  - `login(email, password)` → POST /api/auth/login
  - `logout()` → POST /api/auth/logout
  - `refreshToken()` → POST /api/auth/refresh
  - `getGoogleAuthUrl()` → GET /api/auth/google
  - `forgotPassword(email)` → POST /api/auth/forgot-password
  - `resetPassword(token, newPassword)` → POST /api/auth/reset-password
- Each function returns Promise with response data
- Handle errors and return error messages

### 33. Create User Service Layer
- Create `app/client/src/services/userService.js`
- Implement API functions:
  - `getCurrentUser()` → GET /api/users/me
  - `updateProfile(data)` → PATCH /api/users/me
- Each function returns Promise with response data

### 34. Create Auth Composable
- Create `app/client/src/composables/useAuth.js`
- Export `useAuth()` composable that returns:
  - `isAuthenticated` - Reactive boolean
  - `user` - Reactive user object
  - `login(email, password)` - Call authService.login() and update store
  - `register(data)` - Call authService.register()
  - `logout()` - Call authService.logout() and clear store
  - `forgotPassword(email)` - Call authService.forgotPassword()
  - `resetPassword(token, password)` - Call authService.resetPassword()
- Handle loading states and error messages

### 35. Create Google OAuth Composable
- Create `app/client/src/composables/useGoogleAuth.js`
- Export `useGoogleAuth()` composable that returns:
  - `loginWithGoogle()` - Get authorization URL and redirect to Google
  - `handleGoogleCallback(code)` - Handle OAuth callback
- Implement popup and redirect flows
- Update auth store after successful OAuth

### 36. Create Login Form Component
- Create `app/client/src/components/LoginForm.vue`
- Create form with email and password inputs
- Add submit button
- Implement form validation (required fields, email format)
- Call useAuth().login() on submit
- Display loading state during submission
- Display error messages
- Add link to registration page
- Add link to forgot password page
- Style form with clean, professional design

### 37. Create Register Form Component
- Create `app/client/src/components/RegisterForm.vue`
- Create form with email, password, first name, last name inputs
- Add password confirmation field
- Implement form validation:
  - Required fields
  - Email format
  - Password strength (8+ chars, 1 uppercase, 1 number)
  - Passwords match
- Call useAuth().register() on submit
- Display loading state during submission
- Display success message on successful registration
- Display error messages
- Add link to login page
- Style form consistently with LoginForm

### 38. Create Google Login Button Component
- Create `app/client/src/components/GoogleLoginButton.vue`
- Create styled "Sign in with Google" button
- Use Google branding guidelines
- Call useGoogleAuth().loginWithGoogle() on click
- Display loading state
- Handle errors

### 39. Create Forgot Password Form Component
- Create `app/client/src/components/ForgotPasswordForm.vue`
- Create form with email input
- Implement form validation
- Call useAuth().forgotPassword() on submit
- Display success message (always, for security)
- Add link to login page
- Style form consistently

### 40. Create Reset Password Form Component
- Create `app/client/src/components/ResetPasswordForm.vue`
- Create form with new password and confirm password inputs
- Implement password validation
- Extract token from route params
- Call useAuth().resetPassword() on submit
- Display success message and redirect to login
- Display error messages
- Style form consistently

### 41. Create User Profile Component
- Create `app/client/src/components/UserProfile.vue`
- Display user information (name, email, role, tenant)
- Display auth provider (local or Google)
- Add edit profile button (future enhancement)
- Style as card component

### 42. Create Login View
- Create `app/client/src/views/LoginView.vue`
- Layout with centered LoginForm component
- Include GoogleLoginButton component
- Add application branding/logo
- Add decorative elements for professional appearance
- Ensure responsive design

### 43. Create Register View
- Create `app/client/src/views/RegisterView.vue`
- Layout with centered RegisterForm component
- Include GoogleLoginButton component
- Add application branding
- Ensure responsive design

### 44. Create Forgot Password View
- Create `app/client/src/views/ForgotPasswordView.vue`
- Layout with centered ForgotPasswordForm component
- Add application branding
- Ensure responsive design

### 45. Create Reset Password View
- Create `app/client/src/views/ResetPasswordView.vue`
- Layout with centered ResetPasswordForm component
- Add application branding
- Ensure responsive design

### 46. Create Dashboard View
- Create `app/client/src/views/DashboardView.vue`
- Protected route requiring authentication
- Display welcome message with user name
- Display available modules based on subscription plan
- Add navigation to profile page
- Add logout button
- Style as modern dashboard

### 47. Create Profile View
- Create `app/client/src/views/ProfileView.vue`
- Protected route requiring authentication
- Include UserProfile component
- Add back to dashboard button
- Style consistently with dashboard

### 48. Update App.vue
- Replace existing content with router view
- Add global navigation component (if authenticated)
- Add global error/success toast notifications
- Add loading overlay for page transitions
- Style with consistent theme

### 49. Update main.js
- Import and configure Vue Router
- Import and configure Pinia
- Initialize auth store and check authentication on app load
- Mount app with router and pinia plugins

### 50. Create E2E Test - User Registration
- Create `.claude/commands/e2e/test_user_registration.md`
- Follow the pattern from test_basic_query.md
- Define User Story for registration
- Define Test Steps:
  1. Navigate to registration page
  2. Verify registration form elements present
  3. Enter registration data (email, password, first name, last name)
  4. Take screenshot of filled form
  5. Submit registration
  6. Verify success message displayed
  7. Take screenshot of success message
- Define Success Criteria
- Request 2 screenshots minimum

### 51. Create E2E Test - User Login
- Create `.claude/commands/e2e/test_user_login.md`
- Define User Story for login
- Define Test Steps:
  1. Navigate to login page
  2. Verify login form elements present (email, password, Google button)
  3. Enter login credentials
  4. Take screenshot of filled form
  5. Submit login
  6. Verify redirect to dashboard
  7. Verify user name displayed in dashboard
  8. Take screenshot of dashboard
  9. Click logout button
  10. Verify redirect to login page
- Define Success Criteria
- Request 3 screenshots minimum

### 52. Create E2E Test - Password Reset
- Create `.claude/commands/e2e/test_password_reset.md`
- Define User Story for password reset
- Define Test Steps:
  1. Navigate to login page
  2. Click "Forgot Password" link
  3. Verify forgot password form
  4. Enter email address
  5. Take screenshot of form
  6. Submit request
  7. Verify success message
  8. Take screenshot of success message
  9. Manually extract reset token from server logs (documented in test)
  10. Navigate to reset password page with token
  11. Enter new password
  12. Submit reset
  13. Verify success message and redirect to login
  14. Take screenshot
  15. Login with new password
  16. Verify successful login
- Define Success Criteria
- Request 4 screenshots minimum

### 53. Create E2E Test - Google OAuth
- Create `.claude/commands/e2e/test_google_oauth.md`
- Define User Story for Google OAuth
- Define Test Steps (note: requires Google test account):
  1. Navigate to login page
  2. Take screenshot of initial page
  3. Click "Sign in with Google" button
  4. Verify redirect to Google OAuth consent screen (external)
  5. Document manual Google login steps (cannot automate fully)
  6. After OAuth callback, verify redirect to dashboard
  7. Verify user profile shows auth_provider as 'google'
  8. Take screenshot of dashboard
  9. Take screenshot of profile page
- Define Success Criteria
- Note that full OAuth testing requires manual intervention
- Request 3 screenshots minimum

### 54. Run All Backend Tests
- Run `cd app/server && uv run pytest -v` to execute all unit tests
- Verify all tests pass
- Check test coverage (should be >80% for critical paths)
- Fix any failing tests before proceeding

### 55. Run Frontend Type Check and Build
- Run `cd app/client && bun run tsc --noEmit` (if using TypeScript)
- Run `cd app/client && bun run build` to ensure frontend builds successfully
- Fix any build errors

### 56. Start Application Services
- Ensure Docker services are running: `docker compose up -d`
- Start backend server locally: `cd app/server && uv run uvicorn main:app --reload --port 8000`
- Start frontend dev server: `cd app/client && bun run dev`
- Verify backend accessible at http://localhost:8000
- Verify frontend accessible at http://localhost:5173
- Check API docs at http://localhost:8000/docs

### 57. Execute E2E Test - User Registration
- Read `.claude/commands/test_e2e.md`
- Read `.claude/commands/e2e/test_user_registration.md`
- Execute the E2E test using Playwright browser automation
- Capture screenshots as specified
- Save screenshots to agents directory
- Verify all success criteria met
- Document any failures

### 58. Execute E2E Test - User Login
- Read `.claude/commands/test_e2e.md`
- Read `.claude/commands/e2e/test_user_login.md`
- Execute the E2E test using Playwright browser automation
- Capture screenshots as specified
- Verify all success criteria met
- Document any failures

### 59. Execute E2E Test - Password Reset
- Read `.claude/commands/test_e2e.md`
- Read `.claude/commands/e2e/test_password_reset.md`
- Execute the E2E test using Playwright browser automation
- Capture screenshots as specified
- Verify all success criteria met
- Document any failures

### 60. Execute E2E Test - Google OAuth
- Read `.claude/commands/test_e2e.md`
- Read `.claude/commands/e2e/test_google_oauth.md`
- Execute the E2E test using Playwright browser automation
- Note manual steps required for Google OAuth
- Capture screenshots as specified
- Verify success criteria as much as possible
- Document limitations and manual verification steps

### 61. Validate Zero Regressions
- Run full backend test suite: `cd app/server && uv run pytest`
- Verify all tests pass with zero failures
- Run frontend type check: `cd app/client && bun tsc --noEmit`
- Verify no type errors
- Run frontend build: `cd app/client && bun run build`
- Verify build succeeds
- Test existing health endpoint still works: `curl http://localhost:8000/api/health`
- Verify PostgreSQL connection status still works in frontend
- Document any regressions found and fix immediately

### 62. Update Documentation
- Update `README.md` with authentication setup instructions
- Document environment variables required for authentication
- Document Google OAuth setup steps (Google Cloud Console configuration)
- Document default user credentials for testing
- Document JWT token management approach
- Document rate limiting behavior
- Add security considerations section
- Update API endpoint documentation table with auth endpoints
- Add authentication flow diagrams (optional, text-based)

## Testing Strategy

### Unit Tests
**Password Service Tests:**
- Hash password creates different hashes for same input
- Verify password succeeds with correct password
- Verify password fails with incorrect password
- Validate password strength accepts valid passwords (8+ chars, uppercase, number)
- Validate password strength rejects weak passwords

**Token Service Tests:**
- Create access token includes correct claims and expiry
- Verify access token succeeds with valid token
- Verify access token fails with expired token
- Verify access token fails with invalid signature
- Create refresh token stores in database with correct expiry
- Verify refresh token succeeds with valid token
- Verify refresh token fails with revoked token
- Revoke refresh token marks as revoked in database

**Rate Limiting Tests:**
- Rate limit allows requests under threshold (5 attempts)
- Rate limit blocks after threshold exceeded
- Rate limit returns correct remaining attempts
- Rate limit resets after successful login
- Rate limit expires after lockout period (15 minutes)

**User Service Tests:**
- Create user with local auth provider hashes password
- Create user with Google auth provider has null password
- Create user fails with duplicate email
- Get user by email returns correct user
- Get user by Google ID returns correct user
- Update last login updates timestamp and resets failed attempts
- Get user profile includes tenant, role, and permissions

**Authentication Service Tests:**
- Register user creates user with correct defaults (loan_officer role, local provider)
- Register user validates password strength
- Register user fails with duplicate email
- Login succeeds with correct credentials and returns tokens
- Login fails with incorrect password
- Login fails when rate limit exceeded
- Login fails for Google users trying password login
- Logout revokes refresh token
- Token refresh returns new tokens and rotates refresh token
- Token refresh fails with invalid refresh token
- Password reset request generates token and logs URL
- Password reset request always returns success (security)
- Password reset succeeds with valid token
- Password reset fails with expired token
- Password reset fails with used token

**OAuth Service Tests:**
- Get Google authorization URL returns valid URL with correct parameters
- Exchange code for token calls Google API correctly (mocked)
- Get Google user info extracts correct fields (mocked)
- OAuth error handling returns appropriate errors

**Integration Tests:**
- Full registration flow (POST /auth/register) creates user
- Full login flow (POST /auth/login) returns tokens
- Logout flow (POST /auth/logout) revokes token
- Token refresh flow (POST /auth/refresh) rotates tokens
- Get current user (GET /users/me) returns profile data
- Protected endpoint without token returns 401
- Protected endpoint with invalid token returns 401
- Protected endpoint with valid token returns 200
- Password reset request flow generates token
- Password reset flow updates password
- Rate limiting on login endpoint blocks after 5 attempts

### Edge Cases
- User tries to register with existing email → 409 Conflict
- User tries to login with wrong password 5 times → Rate limited for 15 minutes
- Google user tries to login with password → Error message directing to Google
- Local user tries to login via Google with same email → Error message directing to password login
- User tries to use expired access token → 401 Unauthorized, should trigger refresh
- User tries to use expired refresh token → 401 Unauthorized, must login again
- User tries to use revoked refresh token → 401 Unauthorized
- User tries to reset password with expired token → 400 Bad Request
- User tries to reset password with already-used token → 400 Bad Request
- User tries to reset password for Google account → Error message directing to Google
- User registers with weak password → Validation error with specific requirements
- User submits invalid email format → Validation error
- Access token includes invalid claims → Token verification fails
- Database connection fails during authentication → Graceful error handling
- Redis connection fails for rate limiting → Graceful degradation or error
- Google OAuth API returns error → User-friendly error message
- Session expires while user is active → Automatic token refresh
- User has multiple active sessions → All sessions valid until token expiry
- Admin tries to access super_admin endpoint → 403 Forbidden
- User tries to update another user's profile → 403 Forbidden

## Acceptance Criteria

### AC-1: User Registration (Email/Password) ✓
- New users can register with email, password, first name, last name via POST /api/auth/register
- Email uniqueness enforced at database level and application level (409 error on duplicate)
- Password validation enforces: minimum 8 characters, at least 1 uppercase letter, at least 1 number
- Password hashed using Argon2 algorithm via passlib
- User profile record created automatically with user creation
- Default role assigned: `loan_officer` (from seed data)
- `is_email_verified` set to `false` initially
- `auth_provider` set to `local`
- Registration returns success message without tokens (no auto-login)

### AC-2: User Login (Email/Password) ✓
- Users login via POST /api/auth/login with email and password
- Successful login returns:
  - JWT access token (15 min expiry) in response body
  - JWT refresh token (7 days expiry) in HTTPOnly cookie
  - `last_login_at` timestamp updated in database
- Failed login returns generic "Incorrect email or password" message (no info leakage)
- Rate limiting implemented: 5 failed attempts = 15 minute lockout (Redis-based)
- Users with `auth_provider=google` cannot login with password (validation check)

### AC-3: Google OAuth Login/Registration ✓
- "Sign in with Google" button in frontend redirects to Google OAuth
- Backend GET /api/auth/google returns authorization URL
- Backend GET /api/auth/google/callback handles OAuth callback
- On successful Google auth:
  - If email exists with `auth_provider=google`: User logged in
  - If email exists with `auth_provider=local`: Error "Account exists. Please login with password."
  - If email doesn't exist: Auto-register new user
- Auto-registration extracts: email, given_name, family_name, picture
- Auto-registered user fields set:
  - `auth_provider` = `google`
  - `google_id` = Google's unique user ID
  - `is_email_verified` = `true`
  - `password_hash` = `null`
  - Profile `avatar_url` = Google picture URL
- Returns JWT tokens same as email/password login
- Frontend supports both popup and redirect flows

### AC-4: Token Refresh ✓
- POST /api/auth/refresh endpoint accepts refresh token from HTTPOnly cookie
- Returns new access token (15 min expiry)
- Implements refresh token rotation: new refresh token issued, old one revoked
- Invalid/expired refresh token returns 401 Unauthorized
- Works identically for both local and Google auth users
- Frontend automatically refreshes token on 401 errors via Axios interceptor

### AC-5: Logout ✓
- POST /api/auth/logout endpoint invalidates refresh token
- Refresh token marked as revoked in database
- Refresh token cookie cleared
- Access token remains valid until expiry (stateless JWT characteristic)
- Optional: Google OAuth token revocation implemented for enhanced security

### AC-6: Forgot Password ✓
- POST /api/auth/forgot-password accepts email
- Only works for users with `auth_provider=local`
- Google users receive message: "Please sign in with Google"
- Generates secure UUID reset token with 1-hour expiry
- Reset token stored in database
- Reset link logged to console (no email service for MVP)
- Always returns success message to prevent email enumeration

### AC-7: Reset Password ✓
- POST /api/auth/reset-password accepts token and new_password
- New password validated against security requirements
- Reset token single-use: marked as used after successful reset
- Expired/invalid token returns 400 Bad Request with clear message
- Only available for `auth_provider=local` users
- Password hash updated in database

### AC-8: Get Current User ✓
- GET /api/users/me requires valid access token
- Returns comprehensive profile:
  - User details: id, email, first_name, last_name, auth_provider
  - Tenant info: company_name, plan
  - Role info: role name, permissions list
  - Available modules based on subscription plan
- `auth_provider` field indicates `local` or `google`
- Returns 401 if not authenticated

### AC-9: Link/Unlink Google Account (Future Enhancement) 🔄
- Documented as future enhancement
- Would allow local users to link Google account
- Would allow Google users to set password for local login
- Not implemented in MVP scope

## Validation Commands
Execute every command to validate the feature works correctly with zero regressions.

1. **Run backend unit and integration tests:**
   ```bash
   cd app/server && uv run pytest -v
   ```
   All tests must pass with zero failures.

2. **Run frontend type check:**
   ```bash
   cd app/client && bun tsc --noEmit
   ```
   No type errors should be reported.

3. **Run frontend build:**
   ```bash
   cd app/client && bun run build
   ```
   Build must succeed without errors.

4. **Verify database migration:**
   ```bash
   cd app/server && uv run alembic current
   ```
   Should show the current migration version (001_initial_auth_schema).

5. **Test backend API manually:**
   ```bash
   # Start services
   docker compose up -d
   cd app/server && uv run uvicorn main:app --reload --port 8000

   # Test health endpoint (existing functionality)
   curl http://localhost:8000/api/health

   # Test registration
   curl -X POST http://localhost:8000/api/auth/register \
     -H "Content-Type: application/json" \
     -d '{"email":"test@example.com","password":"Test1234","first_name":"Test","last_name":"User"}'

   # Test login
   curl -X POST http://localhost:8000/api/auth/login \
     -H "Content-Type: application/json" \
     -d '{"email":"test@example.com","password":"Test1234"}' \
     -c cookies.txt

   # Test get current user (use access_token from login response)
   curl http://localhost:8000/api/users/me \
     -H "Authorization: Bearer <access_token>" \
     -b cookies.txt
   ```

6. **Execute E2E Test - User Registration:**
   - Read `.claude/commands/test_e2e.md`
   - Read and execute `.claude/commands/e2e/test_user_registration.md`
   - Verify all success criteria met
   - Verify screenshots captured

7. **Execute E2E Test - User Login:**
   - Read `.claude/commands/test_e2e.md`
   - Read and execute `.claude/commands/e2e/test_user_login.md`
   - Verify login, dashboard access, and logout work correctly
   - Verify screenshots captured

8. **Execute E2E Test - Password Reset:**
   - Read `.claude/commands/test_e2e.md`
   - Read and execute `.claude/commands/e2e/test_password_reset.md`
   - Verify forgot password and reset password flows work
   - Verify screenshots captured

9. **Execute E2E Test - Google OAuth:**
   - Read `.claude/commands/test_e2e.md`
   - Read and execute `.claude/commands/e2e/test_google_oauth.md`
   - Verify Google OAuth flow works (manual steps required)
   - Verify screenshots captured

10. **Verify zero regressions:**
    - Verify existing health endpoint still works: `curl http://localhost:8000/api/health`
    - Verify PostgreSQL connection status displayed correctly in frontend
    - Run complete test suite again to ensure no tests broken

## Notes

### Security Considerations
- **Password Hashing:** Using Argon2 (winner of Password Hashing Competition) via passlib for maximum security against rainbow tables and brute force attacks
- **JWT Tokens:** Access tokens have short expiry (15 min) to limit exposure window; refresh tokens stored in HTTPOnly cookies to prevent XSS attacks
- **Token Rotation:** Refresh tokens are rotated on each refresh to detect token theft (if old token used, indicates compromise)
- **Rate Limiting:** Redis-based rate limiting prevents brute force attacks; 5 attempts with 15-minute lockout provides good balance between security and UX
- **Email Enumeration Prevention:** Password reset always returns success to prevent attackers from discovering valid emails
- **CORS Configuration:** Credentials enabled only for frontend origin to prevent CSRF attacks
- **SQL Injection Prevention:** SQLAlchemy ORM with parameterized queries prevents SQL injection
- **Input Validation:** Pydantic schemas validate all inputs to prevent injection attacks

### Multi-Tenancy Design
- Each user belongs to a tenant (organization/company)
- Tenant has a subscription plan (free/basic/premium)
- Available modules determined by tenant's plan
- Future enhancement: Tenant isolation in queries (WHERE tenant_id = current_user.tenant_id)

### Role-Based Access Control (RBAC)
- Three default roles: loan_officer, admin, super_admin
- Permissions associated with roles via many-to-many relationship
- Future enhancement: Fine-grained permissions for specific operations
- Use `require_role()` dependency to protect endpoints

### Dependencies Added
Backend packages installed via `uv add`:
- `sqlalchemy>=2.0.0` - ORM for database operations
- `alembic>=1.13.0` - Database migrations
- `passlib[argon2]>=1.7.4` - Password hashing with Argon2
- `python-jose[cryptography]>=3.3.0` - JWT token encoding/decoding
- `python-multipart>=0.0.6` - Form data parsing for OAuth callback
- `authlib>=1.3.0` - OAuth 2.0 client library for Google integration
- `redis>=5.0.0` - Redis client for rate limiting and caching

Frontend packages installed via `bun add`:
- `vue-router@4` - Routing for Vue 3
- `pinia@2` - State management for Vue 3 (Vuex successor)
- `axios@1` - HTTP client with interceptors
- `@vueuse/core@10` - Vue composition utilities

### Google OAuth Setup Instructions
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create new project or select existing
3. Enable Google+ API
4. Go to Credentials → Create OAuth 2.0 Client ID
5. Set application type to "Web application"
6. Add authorized redirect URIs:
   - `http://localhost:8000/api/auth/google/callback` (local dev)
   - `https://yourdomain.com/api/auth/google/callback` (production)
7. Copy Client ID and Client Secret to `.env` file
8. Set `GOOGLE_CLIENT_ID` and `GOOGLE_CLIENT_SECRET` environment variables

### Future Enhancements
- **AC-9:** Allow users to link/unlink authentication methods (local ↔ Google)
- Email verification flow with email service integration
- Two-factor authentication (2FA) with TOTP
- Session management UI (view active sessions, revoke sessions)
- Password change functionality (for local users)
- Account deletion with data export
- Audit logging for authentication events
- IP-based rate limiting in addition to email-based
- Remember me functionality with longer-lived refresh tokens
- Social login with other providers (Microsoft, GitHub, etc.)
- Enhanced tenant management (invite users, manage roles)
- Fine-grained permissions system

### Testing Notes
- E2E tests require running frontend and backend servers
- Google OAuth E2E test requires Google test account credentials
- Rate limiting tests may be slow due to Redis TTL waiting
- Use pytest fixtures for database test isolation (rollback after each test)
- Mock external APIs (Google OAuth) in unit tests
- Integration tests use TestClient from FastAPI (doesn't require running server)

### Deployment Considerations
- Set `JWT_SECRET_KEY` to cryptographically secure random value in production
- Use Azure Key Vault for storing secrets (GOOGLE_CLIENT_SECRET, JWT_SECRET_KEY)
- Configure CORS allowed origins to production frontend URL only
- Use HTTPS in production (required for HTTPOnly cookies)
- Set secure cookie flags in production (Secure, SameSite=Lax)
- Monitor rate limiting metrics in production
- Set up database backups for user data
- Configure Redis persistence for rate limiting data
- Use connection pooling for database (already configured via PgBouncer)
- Monitor JWT token sizes (avoid storing too much data in tokens)

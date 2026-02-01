# User Authentication & Session Management

**Date:** 2025-12-12
**Specification:** specs/issue-04-planner-user-auth-session-mgmt.md

## Overview

A comprehensive authentication and session management system for the Valargen mortgage automation platform. Supports dual authentication methods: traditional email/password with Argon2 hashing, and Google OAuth 2.0 integration. Implements JWT-based stateless authentication with refresh token rotation, role-based access control (RBAC), multi-tenant architecture, and Redis-powered rate limiting to prevent brute force attacks.

## Screenshots

### Login Page
![Login Page](assets/01_login_page.png)

### Registration Page
![Registration Page](assets/02_registration_page.png)

### Registration CORS Configuration
![Registration CORS Blocker](assets/03_registration_cors_blocker.png)

## What Was Built

### Backend Components
- **Database Models** - User, Tenant, Role, Permission, RefreshToken, PasswordResetToken models with SQLAlchemy ORM
- **Authentication Service** - Complete auth business logic (register, login, logout, password reset, OAuth)
- **Token Service** - JWT access/refresh token generation and validation with rotation
- **Password Service** - Argon2 password hashing and strength validation
- **OAuth Service** - Google OAuth 2.0 integration with authorization and token exchange
- **Rate Limiting Service** - Redis-based rate limiting (5 attempts, 15-minute lockout)
- **User Service** - User management and profile operations
- **API Endpoints** - RESTful authentication and user management endpoints
- **Database Migrations** - Alembic migrations for auth schema
- **Seed Data Script** - Initial roles, permissions, and test admin user

### Frontend Components
- **Vue Router** - Client-side routing with authentication guards
- **Pinia Stores** - Auth and user state management
- **Authentication Forms** - Login, register, forgot password, reset password components
- **Google OAuth Button** - "Sign in with Google" integration
- **Protected Views** - Dashboard and profile views with route guards
- **API Service Layer** - Axios client with token refresh interceptors
- **Composables** - `useAuth()` and `useGoogleAuth()` for reusable logic

### Testing & Documentation
- **E2E Test Specifications** - User registration, login, password reset, Google OAuth flows
- **Quick Start Guide** - AUTH_QUICKSTART.md for rapid setup
- **Implementation Status** - Detailed tracking document

## Technical Implementation

### Files Modified

**Backend Core:**
- `app/server/main.py` - Added auth/users routers, CORS config, Redis health check, startup/shutdown events
- `app/server/database.py` - Extended with SQLAlchemy async session management
- `app/server/pyproject.toml` - Added sqlalchemy, alembic, passlib[argon2], python-jose, authlib, redis, pydantic-settings
- `app/server/.env.sample` - Added JWT secrets, Google OAuth credentials, Redis URL

**Frontend Core:**
- `app/client/src/App.vue` - Replaced with router-view and auth initialization
- `app/client/src/main.js` - Added Vue Router and Pinia initialization
- `app/client/package.json` - Added vue-router, pinia, axios, @vueuse/core

**Backend - New Files:**
- `app/server/config.py` - Pydantic settings for configuration management
- `app/server/models/*.py` - 6 SQLAlchemy models (user, tenant, role, permission, refresh_token, password_reset)
- `app/server/schemas/*.py` - Pydantic request/response schemas
- `app/server/services/*.py` - 6 service modules (auth, user, token, password, oauth, rate_limit)
- `app/server/routers/*.py` - API route handlers (auth, users)
- `app/server/dependencies/auth.py` - FastAPI dependencies for authentication
- `app/server/alembic/` - Database migration framework setup
- `app/server/scripts/seed_data.py` - Initial data seeding script

**Frontend - New Files:**
- `app/client/src/router/index.js` - Vue Router with auth guards
- `app/client/src/stores/*.js` - Auth and user Pinia stores
- `app/client/src/services/*.js` - API client with token management
- `app/client/src/components/*.vue` - 6 auth components (LoginForm, RegisterForm, etc.)
- `app/client/src/views/*.vue` - 6 views (LoginView, DashboardView, ProfileView, etc.)
- `app/client/src/composables/*.js` - Reusable auth logic

**Testing:**
- `.claude/commands/e2e/*.md` - 4 E2E test specifications
- `.claude/commands/test.md` - Updated test runner

**Documentation:**
- `AUTH_QUICKSTART.md` - Quick start setup guide
- `IMPLEMENTATION_STATUS.md` - Comprehensive implementation tracking
- `README.md` - Updated with auth system overview

### Key Changes

**Multi-Factor Authentication System:**
- Argon2 password hashing (PHC winner, strongest available)
- JWT tokens: 15-minute access tokens, 7-day refresh tokens
- HTTPOnly cookies for refresh tokens (XSS protection)
- Token rotation on refresh (theft detection)
- Google OAuth 2.0 integration with auto-registration

**Security Architecture:**
- Rate limiting: 5 failed login attempts = 15-minute lockout
- Email enumeration prevention in password reset
- CORS restricted to frontend origin only
- Input validation via Pydantic schemas
- SQL injection protection via SQLAlchemy ORM

**Multi-Tenant RBAC:**
- Three roles: loan_officer, admin, super_admin
- 19 permissions across 6 modules (Dashboard, Loan Scenarios, Task Management, Forms, Reports, Admin)
- Tenant-based subscription plans (free, basic, premium)
- Module access based on subscription tier

**Database Schema:**
- 6 core tables with proper relationships and indexes
- Async SQLAlchemy with timezone-aware timestamps
- Foreign key constraints and cascades
- Alembic migrations for version control

## How to Use

### Initial Setup

1. **Install Backend Dependencies:**
   ```bash
   cd app/server
   uv add sqlalchemy alembic passlib[argon2] python-jose[cryptography] python-multipart authlib redis pydantic-settings
   ```

2. **Install Frontend Dependencies:**
   ```bash
   cd app/client
   bun add vue-router pinia axios @vueuse/core
   ```

3. **Configure Environment:**
   Create `app/server/.env`:
   ```env
   DATABASE_URL=postgresql://valargen:valargen@localhost:6432/valargen
   REDIS_URL=redis://localhost:6379
   JWT_SECRET_KEY=development-secret-key-change-in-production
   JWT_ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=15
   REFRESH_TOKEN_EXPIRE_DAYS=7
   FRONTEND_URL=http://localhost:5173
   ```

4. **Run Database Migrations:**
   ```bash
   cd app/server
   docker compose up -d postgres redis
   uv run alembic upgrade head
   ```

5. **Seed Initial Data:**
   ```bash
   cd app/server
   uv run python scripts/seed_data.py
   ```
   This creates default roles, permissions, tenant, and admin user.

6. **Start Services:**
   ```bash
   # Terminal 1: Backend
   cd app/server
   uv run uvicorn main:app --reload --port 8000

   # Terminal 2: Frontend
   cd app/client
   bun run dev
   ```

### Using the Authentication System

**Registration:**
- Navigate to http://localhost:5173/register
- Enter email, password (8+ chars, 1 uppercase, 1 number), first name, last name
- Click "Register" - redirected to login on success

**Login (Email/Password):**
- Navigate to http://localhost:5173/login
- Enter registered email and password
- Click "Login" - redirected to dashboard on success
- Access token stored in memory, refresh token in HTTPOnly cookie

**Login (Google OAuth):**
- Click "Sign in with Google" button
- Authorize on Google consent screen
- Auto-redirected to dashboard
- Auto-registration if email not found

**Password Reset:**
- Click "Forgot Password" on login page
- Enter email address
- Check console logs for reset link (MVP - no email service)
- Navigate to reset link, enter new password
- Redirected to login after successful reset

**Logout:**
- Click "Logout" button in dashboard
- Refresh token revoked, redirected to login

### API Endpoints

**Authentication:**
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login with email/password
- `POST /api/auth/logout` - Logout and revoke refresh token
- `POST /api/auth/refresh` - Refresh access token
- `GET /api/auth/google` - Get Google OAuth URL
- `GET /api/auth/google/callback` - OAuth callback handler
- `POST /api/auth/forgot-password` - Request password reset
- `POST /api/auth/reset-password` - Reset password with token

**User Management:**
- `GET /api/users/me` - Get current user profile (requires auth)
- `PATCH /api/users/me` - Update user profile (requires auth)

**Health Check:**
- `GET /api/health` - Database and Redis status

### Testing

**Run Backend Tests:**
```bash
cd app/server
uv run pytest -v
```

**Run E2E Tests:**
```bash
# Execute E2E test specifications using test_e2e.md command
# See .claude/commands/e2e/ for test scenarios
```

**Manual API Testing:**
```bash
# Register user
curl -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"Test1234","first_name":"Test","last_name":"User"}'

# Login
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"Test1234"}' \
  -c cookies.txt

# Get current user (replace TOKEN)
curl http://localhost:8000/api/users/me \
  -H "Authorization: Bearer TOKEN" \
  -b cookies.txt
```

## Configuration

### Required Environment Variables

**Backend (`app/server/.env`):**
- `DATABASE_URL` - PostgreSQL connection string
- `REDIS_URL` - Redis connection string
- `JWT_SECRET_KEY` - Secret key for JWT signing (use strong random value in production)
- `JWT_ALGORITHM` - JWT algorithm (default: HS256)
- `ACCESS_TOKEN_EXPIRE_MINUTES` - Access token expiry (default: 15)
- `REFRESH_TOKEN_EXPIRE_DAYS` - Refresh token expiry (default: 7)
- `FRONTEND_URL` - Frontend origin for CORS (default: http://localhost:5173)

**Google OAuth (Optional):**
- `GOOGLE_CLIENT_ID` - From Google Cloud Console
- `GOOGLE_CLIENT_SECRET` - From Google Cloud Console
- `GOOGLE_REDIRECT_URI` - OAuth callback URL (http://localhost:8000/api/auth/google/callback)

### Google OAuth Setup

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create project or select existing
3. Enable Google+ API
4. Create OAuth 2.0 Client ID (Web application)
5. Add authorized redirect URI: `http://localhost:8000/api/auth/google/callback`
6. Copy Client ID and Secret to `.env`

### Password Requirements

Enforced via `password_service.py`:
- Minimum 8 characters
- At least 1 uppercase letter (A-Z)
- At least 1 number (0-9)

### Rate Limiting

Configured in `rate_limit_service.py`:
- **Threshold:** 5 failed login attempts
- **Lockout Duration:** 15 minutes
- **Storage:** Redis (key: `rate_limit:login:{email}`)
- **Graceful Degradation:** If Redis unavailable, rate limiting disabled with warning

### Default User Credentials

Created by seed data script:
- **Email:** admin@valargen.com
- **Password:** Admin123
- **Role:** super_admin
- **Tenant:** Valargen (Premium plan)

## Notes

### Security Considerations

**Password Security:**
- Argon2 hashing (PHC winner, superior to bcrypt/scrypt)
- Server-side validation prevents client-side bypass
- Never logged or transmitted in plaintext

**Token Security:**
- Short-lived access tokens (15 min) limit exposure window
- HTTPOnly cookies prevent XSS attacks on refresh tokens
- Token rotation detects token theft
- JWT signatures prevent tampering

**Rate Limiting:**
- Prevents brute force password attacks
- Generic error messages prevent email enumeration
- IP-based limiting possible with minor code changes

**CORS Protection:**
- Restricted to specific frontend origins
- Credentials only allowed from trusted domains
- Prevents CSRF attacks

**Input Validation:**
- Pydantic schemas validate all inputs
- SQLAlchemy ORM prevents SQL injection
- Email format validation prevents injection

### Architecture Decisions

**JWT vs Sessions:**
- Chose JWT for stateless authentication (horizontal scaling)
- Refresh tokens in database allow revocation (hybrid approach)
- Access tokens short-lived to minimize breach impact

**Argon2 vs Bcrypt:**
- Argon2 is PHC winner, more resistant to GPU attacks
- Higher memory cost makes cracking impractical
- Industry best practice as of 2025

**Redis for Rate Limiting:**
- Atomic increments and TTL support
- High performance for frequent operations
- Graceful degradation if unavailable

**Multi-Tenant Design:**
- Single database with tenant_id isolation
- Subscription-based feature gating
- Scalable to thousands of tenants

### Known Limitations

**MVP Scope:**
- No email service (password reset links logged to console)
- No email verification (is_email_verified always false for local users)
- No 2FA/MFA support
- No session management UI (view/revoke active sessions)
- No account deletion functionality

**Google OAuth:**
- Requires manual Google Cloud Console setup
- E2E tests require manual intervention for OAuth flow
- Token revocation on logout is optional

**Rate Limiting:**
- Email-based only (not IP-based)
- Redis dependency (disabled if unavailable)
- No distributed rate limiting across multiple backend instances

### Future Enhancements

**Security:**
- Two-factor authentication (TOTP)
- IP-based rate limiting
- Session management (view active sessions, revoke remotely)
- Email verification flow with SendGrid integration
- Password change functionality

**OAuth:**
- Microsoft, GitHub, LinkedIn providers
- Link/unlink authentication methods
- Social profile picture sync

**User Management:**
- Account deletion with data export
- User impersonation for admins
- Audit logging for security events

**Multi-Tenancy:**
- Tenant invitation system
- Custom role creation per tenant
- Fine-grained permission builder

### Troubleshooting

**"Redis unavailable" warning:**
- Ensure Redis running: `docker compose up -d redis`
- Check REDIS_URL in .env matches Docker config
- Rate limiting will be disabled but app continues

**"Invalid token" errors:**
- Check JWT_SECRET_KEY is consistent
- Verify token not expired (access: 15 min, refresh: 7 days)
- Clear cookies and re-login

**"Rate limit exceeded":**
- Wait 15 minutes or clear Redis: `redis-cli FLUSHDB`
- Check failed login count: `redis-cli GET rate_limit:login:{email}`

**CORS errors in frontend:**
- Verify FRONTEND_URL in backend .env matches frontend origin
- Check browser allows credentials (withCredentials: true in axios)
- Ensure backend CORS middleware configured correctly

**Google OAuth not working:**
- Verify Google Cloud Console redirect URI matches backend
- Check GOOGLE_CLIENT_ID and GOOGLE_CLIENT_SECRET in .env
- Ensure Google+ API enabled in Cloud Console

### Deployment Considerations

**Production Security:**
- Generate cryptographically secure JWT_SECRET_KEY (32+ bytes)
- Use Azure Key Vault for secrets
- Enable HTTPS (required for HTTPOnly cookies)
- Set cookie flags: Secure=true, SameSite=Lax
- Restrict CORS to production domain only

**Database:**
- Use connection pooling (PgBouncer already configured)
- Enable SSL/TLS for PostgreSQL connections
- Regular backups of user data
- Monitor for slow queries

**Redis:**
- Enable persistence (AOF or RDB) for rate limiting data
- Use Redis Sentinel or Cluster for high availability
- Monitor memory usage and eviction policies

**Monitoring:**
- Log authentication events (login, logout, failed attempts)
- Alert on unusual patterns (mass failures, rapid logins)
- Track JWT token sizes (avoid storing too much data)
- Monitor rate limiting effectiveness

### Related Documentation

- `AUTH_QUICKSTART.md` - Quick setup guide
- `IMPLEMENTATION_STATUS.md` - Detailed implementation tracking
- `README.md` - Project overview
- `.claude/commands/e2e/*.md` - E2E test specifications
- `specs/issue-04-planner-user-auth-session-mgmt.md` - Original specification

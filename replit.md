# Mortgage Price Analyzer

## Overview

This is a Mortgage Price Analyzer application that integrates with UWM's (United Wholesale Mortgage) Instant Price Quote API. The application allows mortgage brokers to upload customer JSON files or build payloads manually to analyze mortgage quotes, compare pricing options, and find optimal loan terms. The backend is built with Python/Flask, and there's a static HTML/CSS/JS frontend along with configuration scaffolding for a potential React/Vite frontend using shadcn/ui components.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Backend (Python/Flask)

- **Framework**: Flask serves as the backend API server and also serves static files.
- **Entry point**: `main.py` — handles API routes, UWM API integration, and static file serving.
- **Authentication flow**: The app authenticates with UWM's ADFS OAuth2 token endpoint (`sso.uwm.com/adfs/oauth2/token`) using client credentials (username, password, client_id, client_secret, scope) stored in environment variables.
- **API proxy pattern**: The backend acts as a proxy between the frontend and UWM's staging API (`stg.api.uwm.com`). It obtains an OAuth2 token, then forwards price quote requests to UWM's Instant Price Quote v2 endpoint.
- **Proxy support**: The backend supports SOCKS5 proxy configuration via the `SOCKS_PROXY` environment variable for network routing requirements.
- **Session management**: Uses a `requests.Session` object with custom headers and optional proxy configuration for all outbound HTTP calls.

### Frontend (Dual Setup)

There are two frontend approaches present in the repo:

1. **Static HTML/JS/CSS frontend** (currently active, in `static/` directory):
   - Simple vanilla JS application with tab-based navigation
   - Two modes: "Analyze File" (upload JSON) and "Payload Builder" (form-based)
   - Communicates with backend via `/api/analyze` and `/api/analyze/direct` endpoints
   - Users can preview and download generated JSON payloads

2. **React/Vite frontend scaffolding** (partially configured):
   - `components.json` configures shadcn/ui with the "new-york" style
   - Uses TypeScript (`.tsx`), Tailwind CSS with CSS variables
   - Path aliases configured: `@/components`, `@/lib/utils`, `@/hooks`, etc.
   - Build script in `script/build.ts` uses Vite for client and esbuild for server
   - This appears to be scaffolding that hasn't been fully implemented yet

### Key API Endpoints

- `/api/analyze` — Accepts multipart form data with a JSON file upload, plus optional query params (`min_savings`, `target_amount`, `tolerance`). Processes the file against UWM's price quote API.
- `/api/analyze/direct` — Accepts a JSON payload directly (from the payload builder) for analysis.

### UWM API Integration

- **Token endpoint**: `https://sso.uwm.com/adfs/oauth2/token` — OAuth2 token acquisition
- **Price Quote endpoint**: `https://stg.api.uwm.com/public/instantpricequote/v2/pricequote` — Currently pointing to UWM's staging environment
- **Payload structure**: The price quote request includes fields like brokerAlias, loanOfficer, loanAmount, loanTypeIds, salesPrice, creditScore, propertyZipCode, and many other mortgage-specific parameters (see `attached_assets/` for full payload examples)

### Build System

- `package.json` runs `python main.py` as the dev script
- `script/build.ts` handles production builds: Vite for client, esbuild for server
- The build script bundles specific server dependencies (listed in an allowlist) to reduce cold start times

### Environment Variables Required

| Variable | Purpose |
|----------|---------|
| `UWM_USERNAME` | UWM API authentication username |
| `UWM_PASSWORD` | UWM API authentication password |
| `UWM_CLIENT_ID` | OAuth2 client ID |
| `UWM_CLIENT_SECRET` | OAuth2 client secret |
| `UWM_SCOPE` | OAuth2 scope |
| `SOCKS_PROXY` | Optional SOCKS5 proxy URL |

## External Dependencies

### Python Dependencies
- **Flask** — Web framework for API and static file serving
- **requests** — HTTP client for UWM API calls (with SOCKS proxy support via `requests[socks]`)
- **python-dotenv** — Environment variable loading from `.env` files

### JavaScript/Node Dependencies (for React frontend scaffolding)
- **Vite** — Frontend build tool
- **esbuild** — Server-side bundling
- **shadcn/ui** — Component library (new-york style)
- **Tailwind CSS** — Utility-first CSS framework
- **Drizzle ORM** — Database ORM (configured in build but not yet actively used)
- Various other libraries listed in the build allowlist (express, passport, pg, stripe, zod, etc.)

### External Services
- **UWM (United Wholesale Mortgage) API** — Core integration for mortgage price quotes via OAuth2-authenticated REST API (currently using staging environment)
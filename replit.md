# Mortgage Analyzer

A Flask-based mortgage analysis tool with UWM integration and SOCKS proxy tunneling.

## Project Structure
- `main.py`: Entry point, Flask app, and API routes.
- `models.py`: Database models (SQLAlchemy).
- `static/`: Frontend assets (HTML, JS, CSS).
- `valargen-staging_key.pem`: SSH key for SOCKS tunneling.

## Setup
1. Secrets required: `UWM_USERNAME`, `UWM_PASSWORD`, `UWM_CLIENT_ID`, `UWM_CLIENT_SECRET`, `UWM_SCOPE`, `SESSION_SECRET`.
2. Environment variables: `SOCKS_PROXY`, `TOKEN_URL`, `PRICEQUOTE_URL`.

## Tunneling & Publishing
The app is configured to automatically start the SSH tunnel when published. 
The `run` command in the deployment configuration handles this:
`bash -c "chmod 600 valargen-staging_key.pem && ssh -i valargen-staging_key.pem -o StrictHostKeyChecking=no -N -D 1080 vg-stg-user@4.227.184.143 & sleep 10 && python main.py"`

## Running Locally
Use the "Run Mortgage Analyzer" workflow. It handles the tunnel and starts the server on port 5000.

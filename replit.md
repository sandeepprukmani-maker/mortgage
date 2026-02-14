# Mortgage Price Analyzer

## Overview
A Flask web application that analyzes mortgage quotes using customer data. It integrates with UWM (United Wholesale Mortgage) APIs to fetch price quotes and find qualifying mortgage products that offer savings for customers.

## Current State
- Application is fully imported and running
- Uses SQLite database (project.db) for customer storage
- Frontend is a static HTML/CSS/JS app served by Flask
- Has three main views: Database Analysis, Payload Builder, Manage Customers

## Project Architecture
- **main.py** - Main Flask application with all API routes and business logic
- **models.py** - SQLAlchemy models (Customer model with SQLite)
- **static/** - Frontend files (index.html, script.js, style.css)
- **pyproject.toml** - Python dependencies managed by uv

## Key Features
- Customer CRUD operations via REST API
- UWM API integration for mortgage price quotes
- Qualifying product analysis based on monthly savings
- Payload builder for customizing API requests
- Mock response support when API credentials aren't configured

## Environment Variables
- UWM_USERNAME, UWM_PASSWORD, UWM_CLIENT_ID, UWM_CLIENT_SECRET, UWM_SCOPE - UWM API credentials
- SOCKS_PROXY - Optional SOCKS5 proxy for API requests

## Running
- Development: `gunicorn --bind 0.0.0.0:5000 --reuse-port --reload main:app`
- The app serves static files and API endpoints from the same Flask instance

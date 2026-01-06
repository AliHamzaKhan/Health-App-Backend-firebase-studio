#!/bin/bash

# Exit on error
set -e

# Install dependencies
uv pip install -r mediconnect_backend/requirements.txt
uv pip install google-genai pytest httpx pydantic-settings passlib python-multipart pandas

# Run tests
/home/user/health-app-backend-2/.venv/bin/pytest mediconnect_backend/

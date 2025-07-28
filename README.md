# Mistral Fullstack Takehome

A fullstack chat application built with FastAPI, React, and PostgreSQL, featuring Mistral AI integration.

## Architecture

- **Backend**: FastAPI with SQLModel and Alembic for database migrations
- **Frontend**: React with Vite, TypeScript, and Tailwind CSS
- **Database**: PostgreSQL 17
- **AI**: Mistral AI API integration

## Prerequisites

- Docker and Docker Compose
- Mistral API key

## Quick Start

1. **Set up environment variables**:

   **Option A: Copy the example file** (recommended):

   ```bash
   cp .env.example .env
   ```

   Then edit `.env` and add your actual Mistral API key.

   **Option B: Create manually**:
   Create a `.env` file in the root directory with:

   ```bash
   MISTRAL_API_KEY=your_mistral_api_key_here
   ```

   **Get your Mistral API key**:

   - Visit [Mistral AI Console](https://console.mistral.ai/)
   - Create an account or sign in
   - Navigate to API Keys section
   - Create a new API key
   - Copy the key to your `.env` file

2. **Start all services**:

   ```bash
   docker compose up -d
   ```

3. **Access the application**:
   - Web UI: http://localhost
   - API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs OR http://localhost:8000/redoc

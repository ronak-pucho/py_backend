# FastAPI Production Backend API

A complete, production-ready backend API built with Python FastAPI, PostgreSQL (Neon Database), SQLAlchemy, and JWT Authentication.

## Features

- **JWT Authentication**: Secure user signup, login, password change.
- **User Module**: Profile management, update details, delete account, upload profile image.
- **PostgreSQL**: Hosted on Neon DB.
- **Migrations**: Alembic integration.
- **Validation**: Pydantic schema validation.
- **Security**: Passlib (Bcrypt) for password hashing.
- **API Docs**: Auto-generated Swagger UI (/docs) and ReDoc (/redoc).

## Setup Instructions

### 1. Local Development Setup

1. **Clone the repository** (if applicable) or navigate to the project directory.
2. **Create a virtual environment**:
   ```bash
   python -m venv venv
   # On Windows
   venv\Scripts\activate
   # On macOS/Linux
   source venv/bin/activate
   ```
3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
4. **Environment Variables**:
   Copy the `.env.example` file to `.env` and configure your keys. The `.env` file should contain your Neon Database URL and JWT settings.

### 2. Neon Database Connection

Ensure your `.env` contains the provided connection string:
```env
DATABASE_URL=postgresql://neondb_owner:npg_VowB8eH0kTaW@ep-floral-firefly-abgjje1d.eu-west-2.aws.neon.tech/neondb?sslmode=require
```

### 3. Alembic Migrations

To create the initial tables in your database:
```bash
# Create the initial migration file
alembic revision --autogenerate -m "Initial migration"

# Apply the migration to the database
alembic upgrade head
```

### 4. Running Locally

Start the FastAPI server:
```bash
uvicorn app.main:app --reload
```
Access the interactive Swagger UI documentation at: [http://localhost:8000/docs](http://localhost:8000/docs)

### 5. Docker (Optional)

You can run the application using Docker Compose:
```bash
docker-compose up --build
```

### 6. Postman Testing

A `postman_collection.json` file is provided in the root directory. Import it into Postman. Make sure to set the `base_url` variable to `http://localhost:8000` and paste your JWT access token into the `access_token` variable after logging in.

### 7. Production Deployment (Render)

1. Go to [Render](https://render.com/) and create a new **Web Service**.
2. Connect your GitHub repository containing this codebase.
3. Configure the following:
   - **Environment**: Python
   - **Build Command**: `pip install -r requirements.txt && alembic upgrade head`
   - **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
4. **Environment Variables**:
   Add the variables from your `.env` file into the Render dashboard (e.g., `DATABASE_URL`, `JWT_SECRET_KEY`).
5. Deploy the application.

## Folder Structure

\`\`\`
app/
├── main.py
├── database.py
├── config.py
├── dependencies.py
├── models/
│   └── user.py
├── schemas/
│   └── user.py
├── routers/
│   ├── auth.py
│   └── profile.py
├── services/
│   └── user_service.py
├── repositories/
│   └── user_repo.py
├── auth/
│   ├── security.py
│   └── password.py
├── middleware/
│   └── error_handler.py
├── utils/
│   └── exceptions.py
\`\`\`
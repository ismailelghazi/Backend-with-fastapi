# TalAIt Translation Backend

A secure, private translation backend for TalAIt using FastAPI, PostgreSQL, and Hugging Face Inference API.

## Features

- **Authentication**: JWT stored in HTTP-only cookies.
- **Translation**: English <-> French translation using Helsinki-NLP models.
- **Security**: Password hashing with Bcrypt, secure cookie handling.
- **Database**: PostgreSQL for user storage.
- **Dockerized**: Easy deployment with Docker Compose.

## Architecture

1.  **FastAPI**: Handles HTTP requests and routing.
2.  **PostgreSQL**: Stores user credentials (hashed).
3.  **Hugging Face API**: Performs the actual translation.
4.  **JWT**: Manages session state via secure cookies.

### Authentication Flow

1.  **Register**: User sends username/password -> Backend hashes password -> Stores in DB.
2.  **Login**: User sends credentials -> Backend verifies -> Generates JWT -> Sets `access_token` HTTP-only cookie.
3.  **Protected Routes**: Browser automatically sends cookie -> Backend validates JWT -> Grants access.
4.  **Logout**: Backend clears the cookie.

## Setup & Running

### Prerequisites

- Docker & Docker Compose
- Hugging Face API Token

### Environment Variables

Create a `.env` file in the `backend` directory (or set them in `docker-compose.yml`):

```env
POSTGRES_USER=postgres
POSTGRES_PASSWORD=password
POSTGRES_DB=talait
HF_TOKEN=your_hf_token_here
JWT_SECRET=your_jwt_secret
```

### Running Locally

1.  Navigate to the `backend` directory:
    ```bash
    cd backend
    ```

2.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

3.  Start the server using the provided script (Windows):
    ```bash
    .\start_backend.bat
    ```
    Or manually:
    ```bash
    uvicorn app.main:app --reload
    ```
    **Note:** Make sure to run `uvicorn` from the `backend` directory, not `backend/app`.

The API will be available at `http://localhost:8000`.
Docs will be at `http://localhost:8000/docs`.

### Running with Docker

1.  Navigate to the `backend` directory:
    ```bash
    cd backend
    ```

2.  Build and start the services:
    ```bash
    docker-compose up --build
    ```

The API will be available at `http://localhost:8000`.
Adminer (DB GUI) will be at `http://localhost:8080`.

## API Endpoints

- `POST /register`: Create a new user.
- `POST /login`: Authenticate and receive cookie.
- `POST /logout`: Clear authentication cookie.
- `POST /translate`: Translate text (Requires Auth).

## Hugging Face Limits

The free Hugging Face Inference API has rate limits. If you encounter 503 errors, it means the model is loading. If you hit rate limits, consider upgrading to a paid plan or hosting the models yourself.

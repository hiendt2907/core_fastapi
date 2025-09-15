# core_fastapi

FastAPI backend for loyalty system.

## 🚀 Deployment

This project is ready to deploy on [Railway](https://railway.app).

### Environment Variables

| Key           | Description             |
|---------------|-------------------------|
| JWT_SECRET    | Secret key for JWT auth |
| DATABASE_URL  | PostgreSQL connection string |

### Run locally

```bash
uvicorn main:app --reload


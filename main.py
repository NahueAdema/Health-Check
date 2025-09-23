from fastapi import FastAPI
from health import router as health_router

app = FastAPI()

# Registrar el router de health
app.include_router(health_router)

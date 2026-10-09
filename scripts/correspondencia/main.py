from fastapi import FastAPI
from .database import init_db
from .routers import radicados, remitentes

init_db()

app = FastAPI(
    title="API Unidad de Correspondencia SENA (SQLite3 Modular)",
    description="API desacoplada por capas y módulos de rutas para la gestión de correspondencia.",
    version="1.0.0",
)

# Inclusión de routers
app.include_router(remitentes.router)
app.include_router(radicados.router)
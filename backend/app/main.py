from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from app.infrastructure.api.routes import router as game_router
from app.infrastructure.api.auth_router import router as auth_router

# Cargamos variables de entorno desde el archivo .env
load_dotenv()

# Inicializamos la API
app = FastAPI(
    title="TubeRPG API",
    description="Backend Monolito Hexagonal para gamificación de cursos",
    version="1.0.0"
)

# Configuración de CORS (Permitimos todo para desarrollo, luego cerramos)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

# Registro de Routers
app.include_router(game_router, prefix="/api/v1")
app.include_router(auth_router, prefix="/api/v1/auth", tags=["auth"])

# Endpoint para verificar que el contenedor Docker vive
@app.get("/health")
def health_check():
    return {
        "status": "ok", 
        "message": "El backend de FastAPI está corriendo pipí cucú desde el contenedor."
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)

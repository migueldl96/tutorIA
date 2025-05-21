from fastapi import FastAPI

import sys
# Añadir la ruta actual al sys.path
from .evaluation.routes import router as evaluation_router

# Main app
app = FastAPI() 

# Include the evaluation router
app.include_router(evaluation_router)

@app.get("/health")
async def health():
    return {"status": "ok"}

from fastapi import FastAPI
from evaluation.routes import router as evaluation_router
import uvicorn
# Main app
app = FastAPI() 

# Include the evaluation router
app.include_router(evaluation_router)

@app.get("/health")
async def health():
    return {"status": "ok"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=80)
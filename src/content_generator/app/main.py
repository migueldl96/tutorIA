from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import content, quiz_router
from controllers.aisearch_controller import router as aisearch_router
import uvicorn
app = FastAPI(
    title="TutorIA Content Generator API",
    description="API for generating dynamic content for TutorIA",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)



app.include_router(content.router, prefix="/api/v1", tags=["content"])
app.include_router(quiz_router.quiz_router, prefix="/api/v1", tags=["quiz"])
app.include_router(aisearch_router, prefix="/api/v1", tags=["search"])
@app.get("/")
async def root():
    return {"message": "Welcome to Content Generator API"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=80)
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.api.routes import agent

app = FastAPI(
    title="Tech42 Financial Agent API",
    description="API for interacting with the specialized Amazon financial agent.",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust as needed for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(agent.router)

@app.get("/")
async def root():
    return {"message": "Welcome to the Tech42 Financial Agent API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("src.api.app:app", host="0.0.0.0", port=8000, reload=True)

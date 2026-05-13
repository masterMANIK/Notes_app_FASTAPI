from fastapi import FastAPI

# Initialize the FastAPI app
app = FastAPI(
    title="Notes API",
    description="A production-ready Notes API built with FastAPI",
    version="1.0.0"
)

# Define a root route
@app.get("/")
def read_root():
    return {
        "message": "Welcome to the Notes API!",
        "status": "Healthy"
    }

# Define a simple health check route
@app.get("/health")
def health_check():
    return {"status": "ok"}

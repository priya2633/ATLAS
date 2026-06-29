from fastapi import FastAPI

app = FastAPI(
    title="Atlas AI Platform",
    description="Enterprise AI & Data Platform",
    version="1.0.0"
)

@app.get("/")
def root():
    return {
        "message": "Welcome to Atlas 🚀"
    }

@app.get("/health")
def health():
    return {
        "status": "healthy"
    }
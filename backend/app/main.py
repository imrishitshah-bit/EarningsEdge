from fastapi import FastAPI

app = FastAPI(
    title="EarningsEdge API",
    version="1.0.0"
)

@app.get("/")
def home():
    return {
        "status": "online",
        "project": "EarningsEdge",
        "version": "1.0.0"
    }

@app.get("/health")
def health():
    return {
        "status": "healthy"
    }
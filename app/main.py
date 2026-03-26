from fastapi import FastAPI
from app.api.v1.router import router as v1_router

app = FastAPI(title="TaskFlow API")

# Check if the server is responding or not
@app.get('/ping')
def ping():
    return {"message" : "Pong"}


app.include_router(v1_router, prefix='/api/v1')

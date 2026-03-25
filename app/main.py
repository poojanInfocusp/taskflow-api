from fastapi import FastAPI
from app.api.v1 import auth

app = FastAPI(title="My Taskflow Api")

# Check to see if the Server is running or not
@app.get("/is/server/running")
def is_server_running():
    return {"message" : "Server is running"}

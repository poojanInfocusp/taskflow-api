from fastapi import FastAPI
from config import settings

app = FastAPI()

@app.get('/')
def home():
    print(settings.database_url," = this is the Database URL")
    return {"message" :  "this is home page"} 

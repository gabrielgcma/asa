from fastapi import FastAPI

app = FastAPI()

@app.get("/")

async def root():
    msg = {"response" : "HelloWorld"}
    return msg
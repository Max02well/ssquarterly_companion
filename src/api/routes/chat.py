from fastapi import FastAPI

app = FastAPI()

@app.get("/chat")
async def chat():
    return {"message": "Hello, this is the chat endpoint!"}

@app.post("/chat")
async def chat_post():
    return {"message": "This is a POST request to the chat endpoint!"}
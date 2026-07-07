from fastapi import FastAPI
# pyrefly: ignore [missing-import]
from pydantic import BaseModel

app=FastAPI()

class chatMessage(BaseModel):
    message:str

@app.post("/chat")
def chat(chat:chatMessage):
    return{
        "reply":chat.message
    }
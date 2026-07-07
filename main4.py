from fastapi import FastAPI
# pyrefly: ignore [missing-import]
from pydantic import BaseModel

app = FastAPI()

class StudentResponse(BaseModel):
    id: int
    name: str

@app.get("/student", response_model=StudentResponse)
def get_student():
    return {
        "id": 1,
        "name": "John",
        "age": 22
    }
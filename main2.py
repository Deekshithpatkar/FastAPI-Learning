# POST
from fastapi import FastAPI,Header
# pyrefly: ignore [missing-import]
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

class Student(BaseModel):
    name: str
    age: int



@app.post("/student")
def create_student(student: Student):
    return student


@app.put("/student1/{id}")
def update_student(id: int, student: Student):
    return {
        "id": id,
        "student": student
    }

class StudentUpdate(BaseModel):
    name: Optional[str] = "no update"
    age: Optional[int] = "no update"

@app.patch("/student2/{id}")
def patch_student(id: int, student: StudentUpdate):
    return {
        "id": id,
        "updated_data": student
    }   

@app.delete("/student3/{id}")
def delete_student(id: int):
    return {
        "message": f"Student {id} deleted successfully"
    }
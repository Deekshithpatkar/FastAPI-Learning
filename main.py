#   FASTAPI
from fastapi import FastAPI
app=FastAPI()
@app.get("/")
def home():
    return {"message": "Hello World"}

@app.get("/about")
def about():
    return "Fast API Learning"

@app.get("/contact")
def contact():
    return 1234567899

@app.get("/learning")
def learning():
    return ["Python","UI","FastAPI"]  

@app.get("/nothing")
def nothing():
    print("404 error")

@app.get("/sum")
def sum():
    a=4
    b=5
    answer=a+b
    return answer

@app.get("/student/{id}")
def student(id):
    return {"Student ID": id}

@app.get("/marks/{mark}")
def marks(mark:int):
    return {"Marks": mark}

    
print(app.routes)
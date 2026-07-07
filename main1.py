from fastapi import FastAPI,Header

app=FastAPI()

@app.get("/student/{id}")
def student(id):
    return {"Student ID": id}

@app.get("/marks/{mark}")
def marks(mark:int):
    return {"Marks": mark}

@app.get("/student")
def student(name):
    return {"name":name}

@app.get("/info")
def info(user_agent: str = Header()):
    return {
        "User-Agent": user_agent
    }

@app.get("/info1")
def info1(company: str = Header()):
    return {
        "Company": company
    }
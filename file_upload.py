from fastapi import FastAPI, UploadFile, File

app=FastAPI()

@app.post("/upload")

# upload a file and get the file name
def upload_file(file:UploadFile=File()):
    print(type(file))
    print(file)
    return{
        "filename":file.filename,
        "content_type": file.content_type
    }

# 
@app.post("/uploadawait")
async def upload(file: UploadFile = File()):

    content = await file.read()

    print(type(content))

    return {
        "size": len(content)
    }
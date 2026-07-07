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

# save uploaded file
import shutil
@app.post("/uploadsave")
def upload(file: UploadFile = File()):

    with open(f"uploads/{file.filename}", "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)  #copy from temporary file to new file

    return {
        "message": "File saved successfully",
        "filename": file.filename
    }


#multiple file upload
@app.post("/uploadmultiple")
def upload(file:list[UploadFile]=File()):
    return{
        "total files received":len(file)
    }


#saving multiple files
@app.post("/uploadsavemultiple")
def upload(file:list[UploadFile]=File()):
    for files in file:
        with open(f"uploads/{files.filename}","wb") as buffer:
            shutil.copyfileobj(files.file,buffer)
    return{
        "message": "all files uploaded",
        "total files received": len(file)
    }





from ast import List
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
    uploaded_files=[]
    for files in file:
        with open(f"uploads/{files.filename}","wb") as buffer:
            shutil.copyfileobj(files.file,buffer)
        uploaded_files.append(files.filename)  #to save names of files
        
    return{
        "message": "all files uploaded",
        "total files received": len(file),
        "uploaded_files":uploaded_files
    }



import pandas as pd
# pyrefly: ignore [missing-import]
import fitz
from PIL import Image
# pyrefly: ignore [missing-import]
import cv2
import markdown


# read text file
@app.post("/uploadtxt")
async def upload_txt(file: UploadFile = File()):

    filepath = f"uploads/{file.filename}"

    with open(filepath, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    with open(filepath, "r", encoding="utf-8") as f:
        text = f.read()

    return {
        "filename": file.filename,
        "content": text
    }


# read markdown
@app.post("/uploadmd")
async def upload_md(file: UploadFile = File()):

    filepath = f"uploads/{file.filename}"

    with open(filepath, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    with open(filepath, "r", encoding="utf-8") as f:
        md_text = f.read()

    return {
        "filename": file.filename,
        "markdown": md_text
    }


# read markdown and convert to html
@app.post("/uploadmdhtml")
async def upload_md_html(file: UploadFile = File()):

    filepath = f"uploads/{file.filename}"

    with open(filepath, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    with open(filepath, "r", encoding="utf-8") as f:
        md_text = f.read()

    html = markdown.markdown(md_text)

    return {
        "filename": file.filename,
        "html": html
    }


# read csv
@app.post("/uploadcsv")
async def upload_csv(file: UploadFile = File()):

    filepath = f"uploads/{file.filename}"

    with open(filepath, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    df = pd.read_csv(filepath)

    return {
        "filename": file.filename,
        "rows": df.to_dict(orient="records")
    }


# read excel
@app.post("/uploadexcel")
async def upload_excel(file: UploadFile = File()):

    filepath = f"uploads/{file.filename}"

    with open(filepath, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    df = pd.read_excel(filepath)

    return {
        "filename": file.filename,
        "rows": df.to_dict(orient="records")
    }


# read pdf
@app.post("/uploadpdf")
async def upload_pdf(file: UploadFile = File()):

    filepath = f"uploads/{file.filename}"

    with open(filepath, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    doc = fitz.open(filepath)

    text = ""

    for page in doc:
        text += page.get_text()

    doc.close()

    return {
        "filename": file.filename,
        "text": text
    }


# read image
@app.post("/uploadimage")
async def upload_image(file: UploadFile = File()):

    filepath = f"uploads/{file.filename}"

    with open(filepath, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    image = Image.open(filepath)

    return {
        "filename": file.filename,
        "width": image.width,
        "height": image.height,
        "mode": image.mode,
        "format": image.format
    }


# read video
@app.post("/uploadvideo")
async def upload_video(file: UploadFile = File()):

    filepath = f"uploads/{file.filename}"

    with open(filepath, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    video = cv2.VideoCapture(filepath)

    total_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = video.get(cv2.CAP_PROP_FPS)
    width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))

    video.release()

    return {
        "filename": file.filename,
        "frames": total_frames,
        "fps": fps,
        "width": width,
        "height": height
    }

# read text without saving it
@app.post("/text")
async def upload(file: UploadFile = File()):
    contents = await file.read()
    text = contents.decode("utf-8")
#    md=markdown.markdown(contents)  # for markdown
#    csv=pd.read_csv(contents)  # for csv
#    excel=pd.read_excel(contents)  # for excel
#    doc = fitz.open(stream=contents, filetype="pdf")  # for pdf
#    img = Image.open(io.BytesIO(contents))  # for images
#    video = cv2.VideoCapture(io.BytesIO(contents))  # for videos
    return {
        "text": text
    }


# upload multiple files and process based on file type
@app.post("/uploadmultiplesave")
async def upload(file: list[UploadFile] = File()):

    results = []

    for file in file:

        # ------------------------------------------
        # Save Uploaded File (if you do not want to save the file, remove this section)
        # ------------------------------------------

        filepath = f"uploads/{file.filename}"

        with open(filepath, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # ------------------------------------------
        # PDF
        # ------------------------------------------

        if file.content_type == "application/pdf":

            doc = fitz.open(filepath)

            text = ""

            for page in doc:
                text += page.get_text()

            doc.close()

            results.append({
                "filename": file.filename,
                "type": "PDF",
                "content": text
            })

        # ------------------------------------------
        # IMAGE
        # ------------------------------------------

        elif file.content_type.startswith("image/"):

            image = Image.open(filepath)

            results.append({
                "filename": file.filename,
                "type": "Image",
                "width": image.width,
                "height": image.height,
                "mode": image.mode,
                "format": image.format
            })

        # ------------------------------------------
        # CSV
        # ------------------------------------------

        elif file.filename.endswith(".csv"):

            df = pd.read_csv(filepath)

            df = df.fillna("")

            results.append({
                "filename": file.filename,
                "type": "CSV",
                "rows": df.to_dict(orient="records")
            })

        # ------------------------------------------
        # EXCEL
        # ------------------------------------------

        elif file.filename.endswith(".xlsx"):

            df = pd.read_excel(filepath)

            df = df.fillna("")

            results.append({
                "filename": file.filename,
                "type": "Excel",
                "rows": df.to_dict(orient="records")
            })

        # ------------------------------------------
        # TEXT FILE
        # ------------------------------------------

        elif file.filename.endswith(".txt"):

            with open(filepath, "r", encoding="utf-8") as f:
                text = f.read()

            results.append({
                "filename": file.filename,
                "type": "Text",
                "content": text
            })

        # ------------------------------------------
        # MARKDOWN
        # ------------------------------------------

        elif file.filename.endswith(".md"):

            with open(filepath, "r", encoding="utf-8") as f:
                md_text = f.read()

            html = markdown.markdown(md_text)

            results.append({
                "filename": file.filename,
                "type": "Markdown",
                "markdown": md_text,
                "html": html
            })

        # ------------------------------------------
        # VIDEO
        # ------------------------------------------

        elif file.content_type.startswith("video/"):

            video = cv2.VideoCapture(filepath)

            total_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
            fps = video.get(cv2.CAP_PROP_FPS)
            width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))

            video.release()

            results.append({
                "filename": file.filename,
                "type": "Video",
                "frames": total_frames,
                "fps": fps,
                "width": width,
                "height": height
            })

        # ------------------------------------------
        # Unsupported File
        # ------------------------------------------

        else:

            results.append({
                "filename": file.filename,
                "type": "Unknown",
                "message": "Unsupported file type"
            })

    return {
        "total_files": len(results),
        "files": results
    }
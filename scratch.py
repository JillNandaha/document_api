from fastapi import FastAPI, UploadFile, File 
from app.ingestion import extract_text, chunk_text
from app.vectorstore import add_chunks

app = FastAPI(title="Document Intelligence API")

@app.get("/")
def root():
    return {"status": "alive"}

@app.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    contents = await file.read()
    text = extract_text(file.filename, contents)
    # chunks - list of text chunks embed and store 
    chunks = chunk_text(text)
    # n - integer count of chunks that were succefully added 
    n = add_chunks(doc_id=file.filename, chunks=chunks)
    # return JSON response back to whoever calls /upload endpoint 
    return {"filename": file.filename, "chunks_created": n}
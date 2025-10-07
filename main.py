from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel

from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

# Import or define DocumentIngestion and SemanticSearch
from embeddings import DocumentIngestion
from search import SemanticSearch

import io

app = FastAPI()

ingestion_service = DocumentIngestion()
search_service = SemanticSearch()
print("Ready!")

# Data model for questions
class Question(BaseModel):
    text: str

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def serve_ui():
    return FileResponse("static/index.html")

@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    try:
        # Read file content
        content = await file.read()
        
        # Check file type and extract text
        if file.filename and file.filename.endswith('.txt'):
            try:
                text = content.decode('utf-8')
            except UnicodeDecodeError:
                return {
                    "filename": file.filename,
                    "status": "Error: TXT file is not UTF-8 encoded",
                    "phrases_created": 0
                }
        elif file.filename and file.filename.endswith('.pdf'):
            # Simple PDF text extraction
            try:
                import PyPDF2
                pdf_reader = PyPDF2.PdfReader(io.BytesIO(content))
                text = ""
                for page in pdf_reader.pages:
                    text += page.extract_text() + "\n"
            except ImportError:
                return {
                    "filename": file.filename,
                    "status": "Error: PDF processing requires PyPDF2 - run 'pip install pypdf2'",
                    "phrases_created": 0
                }
            except Exception as e:
                return {
                    "filename": file.filename,
                    "status": f"Error processing PDF: {str(e)}",
                    "phrases_created": 0
                }
        else:
            return {
                "filename": file.filename,
                "status": "Error: Only TXT and PDF files supported",
                "phrases_created": 0
            }
        
        # Process with ML
        phrases_created = ingestion_service.embed_documents(text, file.filename)
        
        return {
            "filename": file.filename,
            "status": "Processed",
            "phrases_created": phrases_created
        }
        
    except Exception as e:
        return {
            "filename": file.filename,
            "status": f"Error: {str(e)}",
            "phrases_created": 0
        }

@app.post("/ask/")
async def ask_question(question: Question):
    # Get all stored phrases
    phrases = ingestion_service.get_all_phrases()
    
    if not phrases:
        return {"answer": "No documents uploaded yet!"}
    
    # Search for answer
    results = search_service.search(question.text, phrases, top_k=1)
    
    if results:
        return {
            "answer": results[0].text,
            "source": results[0].source,
            "confidence": results[0].score
        }
    else:
        return {"answer": "No relevant information found"}

@app.post("/check-completeness/")
async def check_completeness(file: UploadFile = File(...)):
    return {"filename": file.filename, "completeness": "Not implemented yet"}
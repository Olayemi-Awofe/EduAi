from fastapi import FastAPI, HTTPException UploadFile, File, Form
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from utils import *
from fastapi.middleware.cors import CORSMiddleware
from src.database import Base, engine
from src.auth.routes import router as auth_router
from src.school.routes import router as school_router
from src.curriculum.routes import router as curriculum_router
from src.lesson.routes import router as lesson_router
from src.assessments.routes import router as assessments_router
from src.dashboard.routes import router as dashboard_router
from src.upskilling.routes import router as upskilling_router
import os

# Initialize DB tables
Base.metadata.create_all(bind=engine)

# FastAPI app
app = FastAPI()

origins = ['*']
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models for validation
# Request and Response Models

class ChatModel(BaseModel):
    role: str
    message: str

class CreateLesson(BaseModel):
    topic: str
    subject: str
    grade: int
    duration_minutes: int
    lesson_outcome: str
    no_of_questions: int

# Serve the homepage
@app.get("/", response_class=HTMLResponse)
async def home_ui():
    with open("templates/home.html", "r") as file:
        html_content = file.read()
    return HTMLResponse(content=html_content)

# Serve the chatbot page
@app.get("/ai-copilot", response_class=HTMLResponse)
async def chatbot_ui():
    chatbot_file = "templates/copilot.html"
    if not os.path.exists(chatbot_file):
        raise HTTPException(status_code=404, detail="Chatbot file not found.")
    with open(chatbot_file, "r") as file:
        html_content = file.read()
    return HTMLResponse(content=html_content)

# AI Chatbot endpoint
@app.post("/ai-copilot")
async def ai_chatbot(request: ChatModel):
    """
    Endpoint to process insights from analysis and teacher aid recommendation"""
    query = request.message
    if not query:
        raise HTTPException(status_code=400, detail="Chat field cannot be empty.")
    response = chat_ai(query)
    
    # Update chat history
    global chat_history
    chat_history.append({"role": "model", "message": response})

    return {"response": response}

app.include_router(auth_router)
app.include_router(school_router)
app.include_router(curriculum_router)
app.include_router(lesson_router)
app.include_router(assessments_router)
app.include_router(dashboard_router)
app.include_router(upskilling_router)

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from utils import *
from fastapi.middleware.cors import CORSMiddleware

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

class CreateAssessment(BaseModel):
    topic: str
    subject: str
    grade: int
    mcq_count: int

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

# generate-lessons endpoint # Serve the lesson page
@app.get("/generate-lessons", response_class=HTMLResponse)
async def chatbot_ui():
    lesson_file = "templates/lessons.html"
    if not os.path.exists(lesson_file):
        raise HTTPException(status_code=404, detail="Lessons file not found.")
    with open(lesson_file, "r") as file:
        html_content = file.read()
    return HTMLResponse(content=html_content)

@app.post("/generate-lessons")
async def monthly_weekly_goals(request: CreateLesson):
    """
    Endpoint to process teacher input and generate lesson plan and teaching aid.
    """
    topic = request.topic
    subject = request.subject
    grade = request.grade
    duration = request.duration_minutes
    lesson_outcome = request.lesson_outcome

    if not topic or not subject or not grade or not duration or not lesson_outcome:
        raise HTTPException(status_code=400, detail="All field are required.")
    lessons = generate_lessons(topic, subject, grade, duration, lesson_outcome)
    return {"weekly_monthly_goals": lessons}

# generate-assessments endpoint # Serve the assessment page
@app.get("/create-assessment", response_class=HTMLResponse)
async def assessment_ui():
    assessment_file = "templates/assessments.html"
    if not os.path.exists(assessment_file):
        raise HTTPException(status_code=404, detail="Assessments file not found.")
    with open(assessment_file, "r") as file:
        html_content = file.read()
    return HTMLResponse(content=html_content)

@app.post("/create-assessment")
async def generate_assessments(request: CreateAssessment):
    """
    Endpoint to process teacher input and generate assessments.
    """
    topic = request.topic
    subject = request.subject
    grade = request.grade
    no_of_questions = request.mcq_count

    if not topic or not subject or not grade or not no_of_questions:
        raise HTTPException(status_code=400, detail="All fields are required.")

    assessment = create_assessment(topic, subject, grade, no_of_questions)
    return {"assessment": assessment}   
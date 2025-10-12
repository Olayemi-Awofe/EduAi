# Accelerating Educators – Backend & Data Engineering Setup

**Empowering Teachers with Generative AI for Smarter Teaching**

This repository contains the **backend and data engineering** backbone for the **Teacher AI Copilot MVP**, part of the **DataFest Africa 2025 Hackathon Project**:  
**_“Accelerating Educators: AI for Smarter Teaching”_**

---

## Demo Video

[![EduAI Demo](https://img.youtube.com/vi/DhYVuvVn6n8/0.jpg)](https://www.youtube.com/watch?v=DhYVuvVn6n8)

*Click the image above to watch the demo video on YouTube*

**Direct Link:** https://www.youtube.com/watch?v=DhYVuvVn6n8
---

## Frontend Repo
https://github.com/offiongbassey/data-crafters-fe
---

## Test Link
https://eduai-rosy.vercel.app/

## API Docs
https://eduai-e9wp.onrender.com/docs


## Overview

The goal is to build an **AI-powered platform** that helps teachers in Nigeria adapt to the **new skill-based national curriculum** by automatically generating:

- 📚 Lesson plans  
- 🧩 Teaching aids and skill-based pathways  
- 📝 Assessments and tests  
- 📊 Teacher progress tracking  

This backend powers the EduAI platform — handling data ingestion, AI generation (via **Google Gemini**), and secure API endpoints built with **FastAPI**.

---

## Architecture Overview

### 🔹 Core Responsibilities
1. **Data Engineering**
   - Scraping curriculum data from the Nigerian Ministry of Education
   - Generating and cleaning structured datasets for skills, lessons, and assessments
   - Managing ingestion pipelines into PostgreSQL

2. **Backend Engineering**
   - Building scalable REST APIs with **FastAPI**
   - Integrating **Google Gemini API** for generative tasks
   - Handling teacher authentication, skill creation, and content delivery

3. **Generative AI Layer**
   - **Gemini for Lessons:** Generate lesson content, topics, and objectives  
   - **Gemini for Assessments:** Generate quizzes, tests, and evaluation rubrics  
   - **Gemini for Skills:** Create structured learning paths and teacher upskilling modules  

---

## Tech Stack

| Layer | Tools |
|-------|-------|
| **Backend Framework** | FastAPI |
| **Database** | PostgreSQL + SQLAlchemy ORM |
| **AI Model** | Google Gemini API |
| **Data Engineering** | Pandas, NumPy, Faker, BeautifulSoup |
| **Notebook Environment** | JupyterLab |
| **Version Control** | Git + GitHub |
| **Deployment** | Render / Vercel (API endpoint) |

---

## Database Schema

The backend is powered by **PostgreSQL**, with well-defined relationships and constraints.  
Core tables include:

| Table | Description |
|--------|--------------|
| **teachers** | Registered teachers and credentials |
| **schools** | School records and locations |
| **curriculum_units** | Curriculum mapping from the Ministry of Education |
| **lessons** | Lesson content generated via Gemini |
| **assessments** | Tests and questions generated per lesson |
| **skills** | Skill-based pathways for teacher upskilling |
| **sections** | Sections of skills |
| **teacher_progress** | Tracks teacher learning and interaction history |
| **audit_logs** | For monitoring and explainability |
| **test** | Test generated for skill learning |
| **questions** | Generated questions test |


---

## End-to-End Data Engineering Workflow

### **Step 1: Data Acquisition & Development**
- Scrape curriculum data from **Ministry of Education** and other public sources.  
- Generate synthetic teacher and school data using **Faker**.  
- Develop CSV datasets aligned with AI generation tasks.

> Tools used: `pandas`, `faker`, `numpy`, `BeautifulSoup`, `requests`

---

### **Step 2: Initialize Database**
Run the following to initialize your PostgreSQL schema:

```bash
python db/db_init.py
```

## Environmental Variables
```bash
DATABASE_URL=postgresql://<user>:<password>@<host>:<port>/<database>
GEMINI_API_KEY=<your_google_gemini_key>
```

## Quick Start
```bash
# Install dependencies
pip install -r requirements.txt

# Run database initialization
python db/db_init.py

# Start FastAPI server
uvicorn src.main:app --reload
```
Visit http://localhost:8000/docs
 to test the API.

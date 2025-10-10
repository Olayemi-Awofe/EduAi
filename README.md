Accelerating Educators – Data Engineering Setup

# Overview

This repository contains the Data Engineering backbone for the Teacher AI Copilot MVP part of the DataFest Africa 2025 Hackathon project:
“Accelerating Educators: AI for Smarter Teaching”

The objective is to build an AI-powered system that assists teachers in adapting to Nigeria’s new skill-based curriculum by generating lesson plans, teaching aids, assessments, and tracking teacher progress.

As the Data Engineer, this repo focuses on designing, simulating, and managing all data operations — from database schema creation, to synthetic data generation, ingestion, and pipeline automation.

⚙️ End-to-End Data Engineering Workflow
Step 1: Getting all the necessary data, scrapping Ministry of Education, And developing data to meet what we are buidling

The specific table:

Teachers 

Schools 

Curriculum Units 

Lessons 

Assessments 

Teacher Progress 

Audit Logs 


Tools: pandas, faker, numpy, Beautiful soup, sqlite, and many other.

Step 2: Initialize the Database

Run db/db_init.py

This creates a normalized SQLite database (teacher_ai.db) that mirrors real-world relational structure.

Core tables:

teachers

schools

curriculum_units

lessons

assessments

teacher_progress

audit_log

## Schema defines foreign key relationships and metadata tracking for explainability, trust, and accountability.

Step 3: Ingest Data into the DB
Run scripts/ingest_data.py
Script reads the scrapped and developed CSVs and loads them into the SQLite database

Handles duplicate checks, schema validation, and type consistency

Output: edu_ai.db file stored inside /db folder.
This file can be shared across teammates for developement and Repo.

Step 4: Data Access & Collaboration

The SQLite DB can be queried directly using:
import sqlite3
conn = sqlite3.connect("db/edu_ai.db")


Other team members (ML, Backend, or Frontend) can use this same DB file to build and test:
- The Lesson Plan Generator
- Teacher Copilot chatbot
- Dashboard analytics

Since SQLite is file-based, the .db file can be shared, versioned, or rebuilt easily from scratch using your scripts.

Folder Structure
teacher_ai_project/
│
├── README.md                  → Documentation & setup guide  
├── requirements.txt            → Python dependencies  
├── .gitignore                  → Ignored files (env, db, cache)
│
├── db/
│   ├── db_init.py              → Creates database schema  
│   └── edu_ai.db               → Generated SQLite database
│   └── ingest_data.py          → ingest all the tables into SQLite database
│
├── notebooks/
│   └── data_dev.ipynb          → Scrapper and Data dev notebook 
│   └── curriculum.txt          → Numbers of curriculum scrapped from the Ministry of Education
│   └── data_dev.ipynb          → Scrapper and Data dev notebook 
│   └── testing.ipynb           → To test and query my DataBase
│   └── questions_bank.json     → The question and answer of each subject scrap from the internet, exams bodies in Nigeria.

│
├── data/                       → Stores exported datasets (CSV/JSON/PDf)
└── curriculum.pdf              → Stored the scrapped all Curriculums pdfs of each levels and subject.
└── The .csvs                   → All the scrapped and developped data
│
├── scripts/
│   └── ingest_data.py          → Loads data into database
│   ├── db_init.py              → Creates database schema  

│
└── src/
    ├── config.py               → DB connection & constants  
    └── utils.py                → Helper functions (logging, UUIDs, etc.)

Tech Stack
Layer	Tools
Database	SQLite, SQLAlchemy
Scripting	Python 3.10+
Notebook	Jupyter Lab / Jupyter Notebook
Version Control	Git + GitHub

Collaboration Guide

The SQLite DB can be shared via GitHub.

Author & Maintainer
Data Engineer: Olayemi Olusegun Awofe
Hackathon: DataFest Africa 2025
Project: AI for Smarter Teaching (Teacher AI Copilot)

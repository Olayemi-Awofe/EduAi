Accelerating Educators – Data Engineering Setup

# Overview

This repository contains the Data Engineering backbone for the Teacher AI Copilot MVP — part of the DataFest Africa 2025 Hackathon project:
“Accelerating Educators: AI for Smarter Teaching”

The objective is to build an AI-powered system that assists teachers in adapting to Nigeria’s new skill-based curriculum by generating lesson plans, teaching aids, assessments, and tracking teacher progress.

As the Data Engineer, this repo focuses on designing, simulating, and managing all data operations — from database schema creation, to synthetic data generation, ingestion, and pipeline automation.

⚙️ End-to-End Data Engineering Workflow
Step 1: Generate Synthetic Data

Open and run notebooks/synthetic_data_dev.ipynb

Each section creates data for a specific table:

Teachers 

Schools 

Curriculum Units 

Lessons 

Assessments 

Teacher Progress 

Audit Logs 

Export each dataset to /data as CSV or JSON

Tools: pandas, faker, numpy
Purpose: simulate realistic, bias-free data that mimics real teacher, school, and classroom contexts.

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
Script reads generated CSVs and loads them into the SQLite database

Handles duplicate checks, schema validation, and type consistency

Output: teacher_ai.db file stored inside /db folder.
This file can be shared across teammates or regenerated locally using the same scripts.

Step 4: Data Access & Collaboration

The SQLite DB can be queried directly using:
import sqlite3
conn = sqlite3.connect("db/teacher_ai.db")


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
│   └── teacher_ai.db           → Generated SQLite database  
│
├── notebooks/
│   └── synthetic_data_dev.ipynb → Synthetic data generation notebook  
│
├── data/                       → Stores exported datasets (CSV/JSON)
│
├── scripts/
│   └── ingest_data.py          → Loads data into database  
│
└── src/
    ├── config.py               → DB connection & constants  
    └── utils.py                → Helper functions (logging, UUIDs, etc.)

Tech Stack
Layer	Tools
Data Generation	pandas, numpy, faker
Database	SQLite, SQLAlchemy
Scripting	Python 3.10+
Notebook	Jupyter Lab / Jupyter Notebook
Version Control	Git + GitHub

Collaboration Guide

Each teammate clones the repo and runs the notebook locally.

Everyone generates identical synthetic data by using the same random seed and Faker logic.

The SQLite DB can be shared via GitHub or regenerated anytime.

Output Deliverables

teacher_ai.db — Final relational database file

Synthetic CSVs/JSONs in /data

Scripts for database build and ingestion

Fully reproducible workflow for team integration

Author & Maintainer
Data Engineer: Olayemi Olusegun Awofe
Hackathon: DataFest Africa 2025
Project: AI for Smarter Teaching (Teacher AI Copilot)


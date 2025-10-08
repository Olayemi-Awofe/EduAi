import sqlite3
import pandas as pd
import os

# --- Path to data folder
data_folder = r"C:\Users\HP\Desktop\EduAi\data"

# --- SQLite database
db_path = r"C:\Users\HP\Desktop\EduAi\db\edu_ai.db"
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# --- Helper function to load CSV to SQLite
def load_csv_to_sqlite(filename, table_name):
    file_path = os.path.join(data_folder, filename)
    df = pd.read_csv(file_path)
    df.to_sql(table_name, conn, if_exists="replace", index=False)
    print(f"[✅] Loaded {filename} into table '{table_name}'")

# --- Load all tables
tables = [
    ("schools.csv", "schools"),
    ("teachers.csv", "teachers"),
    ("curriculum_units.csv", "curriculum_units"),
    ("lessons.csv", "lessons"),
    ("assessments.csv", "assessments"),
    ("teacher_progress.csv", "teacher_progress"),
    ("audit_log.csv", "audit_log")
]

for file_name, table_name in tables:
    load_csv_to_sqlite(file_name, table_name)

# --- Close connection
conn.commit()
conn.close()
print("\All data ingested into SQLite database successfully!")

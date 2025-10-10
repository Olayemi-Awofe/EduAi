from dotenv import load_dotenv
import os
import json
import google.generativeai as genai
import re

# Load environment variables from .env file
load_dotenv()

# Read secret keys from environment variables
gemini_secret_key = os.getenv('GEMINI_SECRET_KEY')
genai.configure(api_key=gemini_secret_key)

# This function takes the chat history based on their most recent conversation.

# Initialize chat_history OUTSIDE the function

CHAT_HISTORY_FILE = "chat_history.json"
USER_HISTORY_FILE = "user_history.json"

# Load chat history from file or initialize an empty list
def load_chat_history():
    if os.path.exists(CHAT_HISTORY_FILE): # Check if the file exists
        with open(CHAT_HISTORY_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    return [] # Return an empty list if file doesn't exist

# Load user history from file
def load_user_history():
    if os.path.exists(USER_HISTORY_FILE):
        with open(USER_HISTORY_FILE, "r" ) as file:
            return json.load(file)
    return []  

MAX_HISTORY = 5  # Keep only the most recent 5 messages

def save_chat_history():
    # Trim chat history to the last MAX_HISTORY messages
    global chat_history
    if len(chat_history) > MAX_HISTORY:
        chat_history = chat_history[-MAX_HISTORY:]

    with open(CHAT_HISTORY_FILE, "w", encoding="utf-8") as file:
        json.dump(chat_history, file, ensure_ascii=False, indent=4)

def save_user_history():
    # Trim chat history to the last MAX_HISTORY messages
    global user_history
    if len(user_history) > MAX_HISTORY:
        user_history = user_history[-MAX_HISTORY:]

    with open(USER_HISTORY_FILE, "w", encoding="utf-8") as file:
        json.dump(user_history, file, indent=4)     

# Initialize chat history
chat_history = load_chat_history()

# Initialize user history
user_history = load_user_history()

def manage_chat_history(message=None):
    global chat_history  # Access the global chat_history
    
    # Add new message if provided
    if message:
        chat_history.append(message)
        save_chat_history()  # Save the updated chat history

    # Retrieve the most recent user message in a list
    recent_user_messages = user_history[::-1][:1]

    # Retrieve the most recent model message in a list
    recent_model_messages = [
        msg["message"] for msg in reversed(chat_history) if msg.get("role") == "model"[:1]
    ]
    history_list = list(zip(recent_user_messages, recent_model_messages))

    # Format the history as a numbered list
    formatted_history = [
        f"User: {user}<br>Response: {model}" for i, (user, model) in enumerate(history_list)
    ]
    # Return the list of formatted message 
    return formatted_history

# This function takes the teachers query and provides real time assistance
# based on the insights from the teachers progress analysis.
def chat_ai(message):

    global user_history  # Access the global user_history
    
    # Add new message if provided
    if message:
        user_history.append(message)

    genai.configure(api_key=gemini_secret_key)
    system_prompt = f""" You are an AI-powered assistant who provide support for teachers.
                        Reflect on insights from the teachers progress analysis and provide 
                        recommendations and real time assistance to help teachers improve
                        their teaching skills.
                        If you're asked a totally unrealated question, the response should be,
                        'I may not be able to provide information about this topic'
                        """
    model = genai.GenerativeModel('gemini-2.5-pro', system_instruction=system_prompt)
    chat_response = model.generate_content(message).text
    clean_response = chat_response.replace("**", "").replace("*", "")
    return clean_response

# Function to generate lesson plan and teaching aid based on teacher input
# This function takes the teacher input and provides a structured lesson plan
# and teaching aid to help teachers effectively deliver their lessons.
def generate_lessons_with_assessment(topic, subject, grade, duration, lesson_outcome, no_of_questions=5):
    system_prompt = f"""
   You are an AI Teaching Assistant that generates structured lesson plans and assessments in pure JSON format.
    Based on the following input:
    - Topic: {topic}
    - Subject: {subject}
    - Grade: {grade}
    - Duration: {duration}
    - Learning Outcome: {lesson_outcome}
    - Number of Questions: {no_of_questions}

    Return the output strictly as **valid JSON only** with this structure:
    {{
      "lesson": {{
        "lesson_title": "",
        "subject_and_grade": "",
        "duration": "",
        "lesson_objectives": [],
        "instructional_materials": [],
        "lesson_introduction": "",
        "lesson_development": [
        {{
            "time": "",
            "activity": "",
            "details": ""
        }}
        ],
        "learner_activities": [
        {{
            "time": "",
            "activity": "",
            "details": ""
        }}
        ],
        "summary": "",
        "extension_activity": "",
        "teacher_reflection": ""
      }},
      "assessment": {{
        "no_of_questions": {no_of_questions},
        "questions": [
        {{
            "question": "",
            "options": [
              {{ "a": "" }},
              {{ "b": "" }},
              {{ "c": "" }},
              {{ "d": "" }}
            ],
            "answer": ""
        }}
        ]
      }}
    }}
    Notes:
    - The entire response must be valid JSON only.
    - Ensure lesson and assessment content are aligned to the topic and grade.  
    """

    try:
        model = genai.GenerativeModel("gemini-2.5-pro")
        response = model.generate_content(system_prompt)
        ai_response = response.text.strip()

        # 🧹 Remove markdown ```json or ``` and whitespace
        clean_response = re.sub(r"```(?:json)?|```", "", ai_response, flags=re.IGNORECASE).strip()

        # ✅ Try parsing JSON now
        parsed = json.loads(clean_response)
        if "lesson" in parsed and "assessment" in parsed:
            return parsed
        else:
            return {"lesson": {}, "assessment": {}}

    except json.JSONDecodeError:
        return {"error": "Model did not return valid JSON", "raw_text": ai_response}
    except Exception as e:
        return {"error": str(e)}

# Function to generate assessment based on function generate_lessons
# This function takes the teacher input and provides a structured assessment.
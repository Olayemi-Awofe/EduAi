from dotenv import load_dotenv
import os
import json
import google.generativeai as genai
import fitz  # PyMuPDF for PDF extraction

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

lesson_history = []
def generate_lessons(topic, subject, grade, duration, lesson_outcome):
    """
    Generates a detailed lesson plan and teaching aid based on teacher input.

    """
    system_prompt = f"""
                    You are an AI-assisted Teaching Blueprint that helps teachers design 
                    effective lesson plans and teaching aids for classroom delivery.
                    Based on the following input:
                    - Topic: {topic}
                    - Subject: {subject}
                    - Grade: {grade}
                    - Duration: {duration}
                    - Learning Outcome: {lesson_outcome}

                    Generate a comprehensive and professional output with these sections:
                    1. **Lesson Title**
                    2. **Subject and Grade**
                    3. **Duration**
                    4. **Lesson Objectives**
                    5. **Instructional Materials / Teaching Aids**
                    6. **Lesson Introduction (Engagement Strategy)**
                    7. **Lesson Development (Step-by-Step Teaching Activities)**
                    8. **Learner Activities / Group Work**
                    9. **Assessment / Evaluation Questions**
                    10. **Summary / Conclusion**
                    11. **Extension Activity or Homework**
                    12. **Teacher Reflection Tips**
                    
                    Requirements:
                    - Use clear, structured formatting.
                    - Make content age-appropriate for the specified grade.
                    - Keep it practical and classroom-ready.
                    - If the input is irrelevant or nonsensical, respond with:
                    "I may not be able to help you with this information."
                    """

    try:
        # Initialize the Gemini model (use latest model for richer context)
        model = genai.GenerativeModel("gemini-2.5-pro")

        # Generate the lesson plan and teaching aid
        response = model.generate_content(system_prompt)

        # Extract and clean the text
        ai_response = response.text.strip()
        clean_response = ai_response.replace("**", "").replace("*", "")

        # ✅ Append only the clean response string to lesson history
        lesson_history.append(clean_response)

        return clean_response

    except Exception as e:
        return f"An error occurred while generating the lesson plan: {str(e)}"

# Function to generate assessment based on lessons
# This function takes the teacher input and provides a structured assessment.

# ✅ Get the most recent lesson if it exists
if lesson_history:
    most_recent_lesson = lesson_history[-1]
else:
    print("No lesson history available yet.")

def create_assessment(no_of_questions, content=None):
    """
    Generates a multiple-choice assessment based on the no of question and content.
    """ 
    content = content if content else most_recent_lesson
    system_prompt = f"""
    You are an expert educational assessment designer.
    Using the following course material or lesson context, generate a structured assessment.
    You are an expert AI-assisted Assessment Creator that helps teachers design
    high-quality multiple-choice questions (MCQs) for students.
    Task:
        - Create an assessment with {no_of_questions} multiple-choice questions 
        with the content: {content}
        Guidelines:
        - Each question should have 1 correct answer and 3 plausible distractors.
        - Label options as A, B, C, and D.
        - Provide the correct answer key at the end in this format:
            Q1: B
            Q2: D
            ...
        - Ensure questions are clear, concise, and relevant to the content.
            - If the input is irrelevant or nonsensical, respond with:
            "I may not be able to help you with this information."
            """
    try:
        # Initialize Gemini model
        model = genai.GenerativeModel("gemini-2.5-pro")

        # Generate the MCQ assessment
        response = model.generate_content(system_prompt)

        # Extract and return the generated text
        return response.text.strip()

    except Exception as e:
        return f"An error occurred while generating the assessment: {str(e)}"
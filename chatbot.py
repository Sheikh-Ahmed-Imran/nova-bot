# chatbot.py
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage
from difflib import get_close_matches

# ------------------------------
# Categories for topic detection
# ------------------------------
CATEGORIES = [
    "Academics & Exams",
    "Essays & Applications",
    "Universities & Strategy",
    "Internships & Activities",
    "Documents & Portals",
    "Admissions Results",
    "Advisor Feedback"
]

# ------------------------------
# Few-shot examples to improve accuracy
# ------------------------------
EXAMPLES = [
    {"question": "I scored 1450 on my SAT, is that enough for top US universities?", "category": "Academics & Exams"},
    {"question": "Can you check if my UK personal statement is okay for Oxford?", "category": "Essays & Applications"},
    {"question": "Which universities fit my profile for Economics & Management?", "category": "Universities & Strategy"},
]

# ------------------------------
# Detect topic using LLM
# ------------------------------
def detect_topic(question, client):
    # Build few-shot prompt
    examples_text = "\n".join([f"Q: {ex['question']}\nA: {ex['category']}" for ex in EXAMPLES])
    
    prompt = f"""
You are an AI classifier that ONLY outputs the category of a student question.
Available categories: {', '.join(CATEGORIES)}.

Follow these rules:
1. Only respond with one of the categories, nothing else.
2. Do not explain, do not add extra words.
3. Match the question to the most relevant category.
4. Use these examples as reference:
{examples_text}

Question: "{question}"
Answer:
"""
    topic_resp = client.invoke([HumanMessage(content=prompt)])
    topic = topic_resp.content.strip()

    # Validate response
    if topic not in CATEGORIES:
        matches = get_close_matches(topic, CATEGORIES, n=1)
        topic = matches[0] if matches else "Unknown"

    print(f"[Debug] Detected topic: {topic}")
    return topic

# ------------------------------
# Create Gemini client
# ------------------------------
def create_client(user_api_key):
    return ChatGoogleGenerativeAI(
        model="gemini-2.0-flash",
        google_api_key=user_api_key,
        streaming=False
    )

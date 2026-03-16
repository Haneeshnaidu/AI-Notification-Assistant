import os
import json
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate

# Load environment variables from .env file
load_dotenv()

# Get API key from environment
groq_key = os.getenv("GROQ_API_KEY")

if not groq_key:
    raise ValueError("GROQ_API_KEY not found in environment variables.")

llm = ChatGroq(
    model="groq/compound",
    temperature=0,
    groq_api_key=groq_key
)

prompt = ChatPromptTemplate.from_template("""
You are a personal AI assistant.

Classify the notification as High, Medium, or Low priority.
Summarize it in one short sentence.

Return ONLY valid JSON:

{{
    "priority": "",
    "summary": ""
}}

Notification:
{text}
""")

def analyze_notification(text: str):
    chain = prompt | llm
    response = chain.invoke({"text": text})

    content = response.content.strip()

    try:
        # Try direct parse
        return json.loads(content)
    except:
        # Try extracting JSON from text
        start = content.find("{")
        end = content.rfind("}") + 1
        if start != -1 and end != -1:
            json_str = content[start:end]
            return json.loads(json_str)

        return {
            "priority": "Low",
            "summary": content
        }

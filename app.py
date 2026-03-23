from groq import Groq
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def classify_email(email_text):

    # Reduce token usage (IMPORTANT FIX)
    email_text = email_text[:1500]

    prompt = f"""
Classify this email into one category:

Spam
Urgent
Inquiry

Email:
{email_text}

Return only one word category name.
"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message.content.strip()
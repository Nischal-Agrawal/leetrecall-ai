import os

from dotenv import load_dotenv

from openai import OpenAI

load_dotenv()

client = OpenAI(
    api_key=os.getenv(
        "OPENAI_API_KEY"
    )
)


def generate_ai_advice(
    question,
    forget_probability
):

    prompt = f"""
You are an expert DSA revision coach.

Question:
{question}

Forget Probability:
{forget_probability}

Explain:

1. Why the question is being recommended

2. What topic/pattern may be weak

3. What should be revised next

Keep response under 120 words.
"""

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return (
        response
        .choices[0]
        .message
        .content
    )
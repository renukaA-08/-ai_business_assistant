import os
import json
from google import genai
from google.genai import types

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise RuntimeError("GEMINI_API_KEY is not configured")

client = genai.Client(api_key=api_key)

question = "Which product generated the highest revenue?"

prompt = f"""
You are an intent classifier for a sales analytics chatbot.

Classify the user's question into exactly one of these intents:

- total_revenue
- top_product
- monthly_revenue
- top_region
- monthly_revenue_change
- unknown

Rules:
1. Identify what calculation the user wants.
2. All five supported analytics intents are descriptive analytics.
3. If the question does not match any supported intent, return unknown.
4. Do not calculate or invent any business figures.
5. Return only the requested JSON.

User question: {question}
"""

response = client.models.generate_content(
    model="gemini-3.5-flash-lite",
    contents=prompt,
    config=types.GenerateContentConfig(
        response_mime_type="application/json",
        response_json_schema={
            "type": "OBJECT",
            "properties": {
                "intent": {
                    "type": "STRING",
                    "enum": [
                        "total_revenue",
                        "top_product",
                        "monthly_revenue",
                        "top_region",
                        "monthly_revenue_change",
                        "unknown"
                    ]
                },
                "analytics_type": {
                    "type": "STRING",
                    "enum": ["descriptive"]
                }
            },
            "required": ["intent", "analytics_type"]
        }
    )
)

result = json.loads(response.text)
print(result)
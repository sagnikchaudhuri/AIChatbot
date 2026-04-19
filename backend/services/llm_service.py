from groq import Groq
from config import GROQ_API_KEY

client = Groq(api_key=GROQ_API_KEY)

def generate_response(user_message, business_info):
    system_prompt = f"""
You are a helpful assistant for {business_info['name']}.

Business details:
Timings: {business_info['timings']}
Location: {business_info['location']}
Pricing: {business_info['pricing']}

Rules:
- Keep answers short and clear
- Be friendly
- If user wants to join/book, ask for name and phone
"""

    completion = client.chat.completions.create(
        model="llama-3.1-8b-instant", 
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message}
        ],
        temperature=0.7,
        max_tokens=200
    )

    return completion.choices[0].message.content
    return res.choices[0].message.content.encode("utf-8").decode("utf-8")
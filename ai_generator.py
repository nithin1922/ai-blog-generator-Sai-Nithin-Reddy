import os
from groq import Groq
from dotenv import load_dotenv
load_dotenv()

# Initialize Groq client using the GROQ_API_KEY environment variable
client = Groq(api_key=os.getenv('GROQ_API_KEY'))

def generate_post(keyword: str, seo: dict) -> str:
    prompt = (
        f"Write a detailed blog post draft about '{keyword}'. "
        f"Include an introduction, 3–5 subheadings with content, and a conclusion. "
        f"Embed three placeholder affiliate links as {{AFF_LINK_1}}, {{AFF_LINK_2}}, {{AFF_LINK_3}}. "
        f"Also mention the following SEO stats: "
        f"search volume is {seo['search_volume']}, keyword difficulty is {seo['keyword_difficulty']}, "
        f"and average CPC is ${seo['avg_cpc']}.")

    response = client.chat.completions.create(
        model='llama3-8b-8192',
        messages=[
            {'role': 'system', 'content': 'You are a helpful blogging assistant.'},
            {'role': 'user', 'content': prompt}
        ]
    )

    return response.choices[0].message.content
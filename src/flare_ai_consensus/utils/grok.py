from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

client = OpenAI(api_key=os.environ.get("GROK_API_KEY"), base_url="https://api.x.ai/v1")

def request_grok(msg):
    return client.chat.completions.create(
                messages=[{
                    "role": "user",
                    "content": msg,
                }],
                model="grok-2-latest",
            )
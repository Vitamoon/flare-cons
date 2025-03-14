from flask import Flask
from flask import request
import requests

from openai import OpenAI
import numpy as np

from dotenv import load_dotenv
import os


load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
base_url = os.getenv("OPENAI_BASE_URL")

client = OpenAI(api_key=api_key, base_url=base_url)

def cosine_similarity(a: list[float], b: list[float]) -> float:
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

app = Flask(__name__)

@app.route("/")
def shapley_estimator():
    models_list: list[str] = ["all", "qwen", "gemini", "gpt", "claude", "mistral", "llama"]
    base = "http://34.174.16.226:80/api/routes/"
    embeddings = {}
    effects = {}
    responses = {}
    msg = request.args.get('msg', default="What is your favorite pokemon?")
    print(msg)
    for model in models_list:
        res = requests.post(f"{base}{model}/", 
            headers={
                'accept': 'application/json',
                'Content-Type': 'application/json'},
            json={
                'system_message': 'Answer the user question, providing as much information as possible while keeping your response short and succinct. You may additionally receive additional information about responses generated by other models. You should take this information into account if you feel it is accurate and helpful, but if you believe the provided information to be false, provide information refuting it. Keep your response under 300 tokens.',
                'user_message': msg
        })
        if not res.ok:
            return "Error in backend</br></br>Ran out of keys?"
        responses[model] = res.json()["response"]
        embeddings[model] = client.embeddings.create(input=responses[model], model="text-embedding-3-small").data[0].embedding
        effects[model] = 1 - cosine_similarity(embeddings["all"], embeddings[model])
    print(effects)
    return str(responses) + "</br></br>" + str(effects)
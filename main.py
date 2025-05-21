# main.py
# What do you want do?
# 1. This program will receive a call matching endpoint, then it will validate it using some hash
# 2. It will read the callers input like : given input summarize etc
# 3. Then It will call openAI or Gemini and return data
# 4. Returns data from the LLM using some agreed upon return format

import os
from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from dotenv import load_dotenv

from openai import OpenAI
import google.generativeai as genai

# Load .env file
load_dotenv()

# Retrieve API keys and caller token
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
EXPECTED_CALLER_TOKEN = os.getenv("CALLER_TOKEN_HASH")

# Initialize clients
openai_client = OpenAI(api_key=OPENAI_API_KEY)
genai.configure(api_key=GEMINI_API_KEY)

# Initialize FastAPI app
app = FastAPI()

# Request model
class PromptRequest(BaseModel):
    prompt: str
    callerTokenHash: str

# Response model
class PromptResponse(BaseModel):
    response: str

@app.post("/generate", response_model=PromptResponse)
async def generate_response(
    request: PromptRequest,
    provider: str = Query("openai", enum=["openai", "gemini"])
):
    # Validate caller token
    if request.callerTokenHash != EXPECTED_CALLER_TOKEN:
        raise HTTPException(status_code=403, detail="Access denied")

    prompt = request.prompt.strip()
    if not prompt:
        raise HTTPException(status_code=400, detail="Prompt cannot be empty.")

    try:
        if provider == "openai":
            response = openai_client.chat.completions.create(
                model="gpt-04-mini",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
                max_tokens=150
            )
            answer = response.choices[0].message.content.strip()

        elif provider == "gemini":
            model = genai.GenerativeModel("gemini-2.0-flash")
            response = model.generate_content(prompt)
            answer = response.text.strip() #Gemini 1.5 Flash

        return PromptResponse(response=answer)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


import traceback
import asyncio
from fastapi import APIRouter, HTTPException
from google import genai
import os
from dotenv import load_dotenv
from data.schemas.AiRequestDTO import AiRequestDTO
import json
load_dotenv()
ask_ai_router = APIRouter()
from data.helpers import system_prompt
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

@ask_ai_router.post("/ask_ai")
async def ask_ai(ai_request : AiRequestDTO):
    print("ask ai is being called")
    try:
        prompt = f"""
   {system_prompt}
    INPUT:
    {json.dumps(ai_request.model_dump())}
"""
        response = await asyncio.to_thread(
            client.models.generate_content,
            model="gemini-flash-latest",
            contents=prompt,
        )
        text = response.text.strip()
        print(text)
        return {
         "response" : text
        }
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500 , detail=str(e))
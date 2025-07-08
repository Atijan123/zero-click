import os
import traceback
from typing import List, Dict
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
from groq import Groq
from fastapi import Request
from vultr_client import create_vm  # Import deployment logic

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY is not set.")

client = Groq(api_key=GROQ_API_KEY)

class UserInput(BaseModel):
    text: str
    role: str = "user"
    conversation_id: str

class DeployRequest(BaseModel):
    bot_name: str

conversations: Dict[str, List[Dict[str, str]]] = {}

@app.post("/chat")
async def chat(user_input: UserInput):
    conv_id = user_input.conversation_id
    if conv_id not in conversations:
        conversations[conv_id] = []

    conversations[conv_id].append({
        "role": user_input.role,
        "content": user_input.text
    })

    try:
        completion = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=conversations[conv_id],
            temperature=1,
            max_tokens=1024,
            top_p=1,
            stream=True
        )

        response_text = ""
        for chunk in completion:
            response_text += chunk.choices[0].delta.content or ""

        conversations[conv_id].append({
            "role": "assistant",
            "content": response_text
        })

        return {
            "response": response_text,
            "conversation_id": conv_id
        }

    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/deploy")
async def deploy_bot(request: Request):
    payload = await request.json()
    bot_name = payload.get("bot_name")

    if not bot_name:
        raise HTTPException(status_code=400, detail="bot_name is required")

    try:
        instance = create_vm(bot_name)
        return {
            "url": f"http://{instance['main_ip']}:8000",
            "status": "VM Created and Docker will run automatically"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Deployment failed: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

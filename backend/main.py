# Dependencies
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import asyncio
from agents.debate_agents import teamConfig, debate

# initialize fast api app
app = FastAPI()

# Allow Streamlit to talk to FastAPI
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_headers=['*'],
    allow_methods=['*']
)

@app.get("/start_debate")
# async def start_debate(topic: str = "Should Companies go fully remote?"):
async def start_debate(topic: str):
    team = await teamConfig(topic)
    messages = []

    async for message in debate(team):
        messages.append(message)

    return {"messages": messages}

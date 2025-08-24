# Import Dependencies
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.base import TaskResult
from autogen_agentchat.conditions import TextMentionTermination
import asyncio
import re

# env variables
import os
from dotenv import load_dotenv
load_dotenv()

async def teamConfig(topic):
    model = OpenAIChatCompletionClient(
    model="gemma2-9b-it",
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1",
    model_info={
        "model_type": "chat_completion",
        "family": "llama",
        "context_length": 131072,
        "vision": False,
        "structured_output": False,
        "function_calling": False,
        "json_output": False
    })

    supporter_prompt=(
        f"You are Victoria. You argue in support of the motion {topic}."
        "You can only give two points per round."
        "Be sure to give the best answer."
        "The judge will decalre the winner at the end of the debate"
    )

    critic_prompt=(
        "You are Daniel. You are debating against Victoria who is the supporter of the debate."
        "You can only give two points per round."
        "You argue against the motion {topic}."
        "Be sure to give the best answer."
        "The judge will decalre the winner at the end of the debate"
    )

    host_prompt=(
        'You are Mercy, the host of a debate between Victoria, a supporter agent, '
        'and Daniel, a critic agent. You will moderate the debate.'
        f' The topic of the debate is {topic}. '
        'At the beginning of each round, announce the round number. '
        'At the beginning of the last round, declare that it will be '
        'the last round. After the last round, announce the winner, thank the audience and exactly '
        'say "TERMINATE".'
    )

    # supporter agent
    supporter_agent=AssistantAgent(
        name="Victoria",
        system_message=supporter_prompt,
        model_client=model
    )

    # critic agent
    critic_agent=AssistantAgent(
        name="Daniel",
        system_message=critic_prompt,
        model_client=model
    )

    host_agent=AssistantAgent(
        name="Mercy",
        system_message=host_prompt,
        model_client=model
    )

    # create teams
    team=RoundRobinGroupChat(
        participants=[host_agent, supporter_agent,critic_agent],
        max_turns=10,
        termination_condition=TextMentionTermination(text="TERMINATE")
    )

    return team

async def debate(team):
    async for message in team.run_stream(task="Start the debate!"):
        if isinstance(message, TaskResult):
            message = f'Stopping reason: {message.stop_reason}'
            yield message
        else:
            message = f'{message.source}: {message.content}'
            yield message

async def main():
    topic = "Should Campanies go fully remote?"
    team = await teamConfig(topic)
    async for message in debate(team):
        print('-' * 20)
        print(message)
        
if __name__ == '__main__':
    asyncio.run(main())

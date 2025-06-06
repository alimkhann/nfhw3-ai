import asyncio
import websockets
from pydantic_ai import Agent
from dotenv import load_dotenv
import os

load_dotenv()

os.makedirs("logs", exist_ok=True)

model = 'openai:gpt-3.5-turbo'
task_agent = Agent(
    model,
    system_prompt=("""
        You are an expert habit coach who specializes in helping people form healthy routines or break bad ones.
        When the user gives a brief description of their goal or current habit, you must:
        1. Identify the user’s goal/habit in one sentence.
        2. Generate a realistic task for today to support that habit.
        3. Provide exactly three difficulty options—Easy, Medium, Hard—each in 2–3 concise sentences.

        Answer in the exact format below (using these headings):

        Easy: <2–3 sentences>
        Medium: <2–3 sentences>
        Hard: <2–3 sentences>

        Send me a text as a proof that you have completed one of the three tasks.

        Be action-oriented, specific to today, and always concise.
    """)
)

async def task_create(habit):
    return await task_agent.run(habit)

async def task_creator():
    async with websockets.connect("ws://localhost:8001") as ws:
        await ws.send("register:task_creator")

        while True:
            habit = await ws.recv()
            print(f"[PydanticAI Task Creator] Habit received: \"{habit}\"")

            task = await task_create(habit)
            print(f"[PydanticAI Task Creator] Today's task to complete:\n{task}")

            await ws.send(f"send:user:{task}")

            with open("logs/task_creator.log", "a") as f:
                f.write(f"===== Habit =====\n{habit}\n\n===== Tasks =====\n{task}\n\n")

asyncio.run(task_creator())

import asyncio
import websockets
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv

load_dotenv()

async def task_validator():
    async with websockets.connect("ws://localhost:8001") as ws:
        await ws.send("register:task_validator")

        while True:
            task_answer = await ws.recv()
            print(f"[LangChain Task Validator] Task answer received:\n{task_answer}")

            llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0)
            validation_result = await llm.ainvoke(
                f"Validate the user's task answer for correctness and completeness:\n\n"
                f"{task_answer}\n\n"
                "Reply in 2–3 sentences indicating whether it satisfies the task and why."
            )
            print("[LangChain Task Validator] Validation complete, sending to user...")

            await ws.send(f"send:user:{validation_result}")

asyncio.run(task_validator())

import asyncio
import websockets

async def user():
    async with websockets.connect("ws://localhost:8001", ping_interval=None) as ws:
        await ws.send("register:user")

        habbit = input("📝 Describe a habit you want to attain: ")
        await ws.send(f"send:task_creator:{habbit}")

        task_message = await ws.recv()
        print(f"\n📋 Today's task to complete (Easy/Medium/Hard):\n{task_message}")

        answer = input("\n\n✍️ Once done, type your proof of completion: ")

        await ws.send(f"send:task_validator:{answer}")

        validation = await ws.recv()
        print(f"\n📋 Validation result:\n{validation}")

asyncio.run(user())
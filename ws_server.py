import asyncio
import websockets

clients = {}

async def handler(websocket):
    try:
        async for message in websocket:
            print(f"[Server] Received: {message}")
            if message.startswith("register:"):
                name = message.split(":", 1)[1]
                clients[name] = websocket
                print(f"[Server] {name} registered.")
            elif message.startswith("send:"):
                parts = message.split(":", 2)
                if len(parts) < 3:
                    print("[Server] Incorrect format of the message.")
                    continue
                _, to, content = parts
                if to in clients:
                    await clients[to].send(content)
                    print(f"[Server] Sent to → {to}")
                else:
                    print(f"[Server] Agent {to} was not found.")
    except Exception as e:
        print(f"[Server] Error: {e}")

async def main():
    async with websockets.serve(handler, "localhost", 8001, ping_interval=None, ping_timeout=None):
        print("✅ WebSocket server running on ws://localhost:8001")
        await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(main())

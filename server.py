import asyncio
import websockets
import json
import os

clients = {}

async def handler(websocket, path):
    async for message in websocket:
        data = json.loads(message)

        if data.get("type") == "set_role":
            clients[websocket] = {
                "role": data["role"],
                "campaign_id": data["campaign_id"]
            }
        elif data.get("type") == "sync_state" and clients[websocket]["role"] == "master":
            # Рассылка игрокам
            campaign_id = clients[websocket]["campaign_id"]
            for ws, info in clients.items():
                if info["campaign_id"] == campaign_id and info["role"] == "player":
                    await ws.send(message)

async def main():
    port = int(os.environ.get("PORT", 8080))
    server = await websockets.serve(handler, "0.0.0.0", port)
    print(f"Сервер запущен на порт {port}")
    await server.wait_closed()

asyncio.run(main())

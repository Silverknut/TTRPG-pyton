import asyncio
import websockets
import json
import os

connected = set()

async def handler(websocket, path):
    connected.add(websocket)
    print(f"Клиент подключился. ID: {id(websocket)}")

    # Отправляем начальное состояние
    await websocket.send(json.dumps({"message": "Добро пожаловать!"}))

    try:
        async for message in websocket:
            data = json.loads(message)
            print(f"Сервер получил: {data}")

            # Рассылаем всем клиентам
            if connected:
                await asyncio.gather(*[client.send(json.dumps(data)) for client in connected])
    except websockets.exceptions.ConnectionClosed:
        pass
    finally:
        connected.remove(websocket)
        print(f"Клиент отключился. ID: {id(websocket)}")

async def main():
    port = int(os.environ.get("PORT", 8080))
    server = await websockets.serve(handler, "0.0.0.0", port)
    print(f"Сервер запущен на порт {port}")
    await server.wait_closed()

asyncio.run(main())

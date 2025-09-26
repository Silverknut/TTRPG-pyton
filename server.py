import asyncio
import websockets
import json

connected = set()

# Состояние игры (тайлы, туман и т.д.)
game_state = {
    "tiles": [],
    "fog": [],
    "players": {}
}

async def handler(websocket, path):
    # Добавляем клиента
    connected.add(websocket)
    print(f"Клиент подключился. ID: {id(websocket)}")

    # Отправляем начальное состояние
    await websocket.send(json.dumps(game_state))

    try:
        async for message in websocket:
            data = json.loads(message)
            print(f"Сервер получил: {data}")

            # Обновляем состояние игры
            if data.get("type") == "move_tile":
                game_state["tiles"].append(data["tile"])
            elif data.get("type") == "update_fog":
                game_state["fog"].append(data["fog"])

            # Рассылаем всем клиентам
            if connected:
                await asyncio.gather(*[client.send(json.dumps(game_state)) for client in connected])
    except websockets.exceptions.ConnectionClosed:
        pass
    finally:
        connected.remove(websocket)
        print(f"Клиент отключился. ID: {id(websocket)}")

async def main():
    server = await websockets.serve(handler, "0.0.0.0", 8080)
    print("Сервер запущен на порт 8080")
    await server.wait_closed()

asyncio.run(main())

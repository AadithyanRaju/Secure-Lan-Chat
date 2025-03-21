import asyncio
import websockets

async def connect_to_peer(ip, port):
    """Connects to a discovered peer and listens for messages."""
    uri = f"ws://{ip}:{port}"
    async with websockets.connect(uri) as websocket:
        print(f"Connected to {uri}")
        try:
            async for message in websocket:
                print(f"Message from {ip}: {message}")
        except websockets.exceptions.ConnectionClosed:
            print(f"Disconnected from {uri}")

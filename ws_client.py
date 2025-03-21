import asyncio
import base64
import websockets
from crypto_utils import encrypt_message, decrypt_message

async def connect_to_peer(ip, port):
    """Connects to a peer and listens for messages."""
    uri = f"ws://{ip}:{port}"
    async with websockets.connect(uri) as websocket:
        while True:
            encrypted_msg = await websocket.recv()
            print("Received:", decrypt_message(encrypted_msg))

async def send_message(peer_ip, peer_port, message):
    """Encrypts and sends a message to a peer."""
    uri = f"ws://{peer_ip}:{peer_port}"
    async with websockets.connect(uri) as websocket:
        await websocket.send(encrypt_message(message))

async def send_file(peer_ip, peer_port, file_path):
    """Sends a file in chunks over WebSocket."""
    uri = f"ws://{peer_ip}:{peer_port}"
    async with websockets.connect(uri) as websocket:
        with open(file_path, "rb") as f:
            data = f.read()
            encoded_file = base64.b64encode(data).decode()
            await websocket.send(f"FILE:{encoded_file}")

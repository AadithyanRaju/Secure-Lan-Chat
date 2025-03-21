import asyncio
import websockets

connected_peers = set()

async def handle_client(websocket, path):
    """Handles incoming WebSocket messages."""
    connected_peers.add(websocket)
    try:
        async for message in websocket:
            print(f"Received: {message}")
            # Relay message to all connected peers
            for peer in connected_peers:
                if peer != websocket:
                    await peer.send(message)
    finally:
        connected_peers.remove(websocket)

async def start_server(port):
    """Starts WebSocket server on the given port."""
    server = await websockets.serve(handle_client, "0.0.0.0", port)
    print(f"WebSocket server running on ws://0.0.0.0:{port}")
    await server.wait_closed()

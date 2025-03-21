import threading
import asyncio
from peer_discovery import broadcast_presence, listen_for_peers
from ws_server import start_server
from ws_client import connect_to_peer

MY_PORT = 50505  # WebSocket Port
peer_list = []

# Start UDP discovery in background threads
threading.Thread(target=broadcast_presence, args=(MY_PORT,), daemon=True).start()
threading.Thread(target=listen_for_peers, args=(peer_list,), daemon=True).start()

# Start WebSocket server
asyncio.run(start_server(MY_PORT))

# Connect to discovered peers
async def connect_to_discovered_peers():
    while True:
        for peer in peer_list:
            ip, port = peer.split(":")
            asyncio.create_task(connect_to_peer(ip, int(port)))
        await asyncio.sleep(5)

asyncio.run(connect_to_discovered_peers())

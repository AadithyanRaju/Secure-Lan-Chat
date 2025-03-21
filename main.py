import sys
import threading
import asyncio
from PyQt5.QtWidgets import QApplication
from peer_discovery import broadcast_presence, listen_for_peers
from ws_server import start_server
from ui import JoinPage

MY_PORT = 50505  # WebSocket Port
peer_list = []

def start_discovery():
    threading.Thread(target=broadcast_presence, args=(MY_PORT,), daemon=True).start()
    threading.Thread(target=listen_for_peers, args=(peer_list,), daemon=True).start()

def start_websocket_server():
    asyncio.run(start_server(MY_PORT))

if __name__ == "__main__":
    # Start Peer Discovery
    start_discovery()

    # Start WebSocket server in a separate thread
    threading.Thread(target=start_websocket_server, daemon=True).start()

    # Start PyQt Application
    app = QApplication(sys.argv)
    window = JoinPage(peer_list)
    window.show()
    sys.exit(app.exec_())

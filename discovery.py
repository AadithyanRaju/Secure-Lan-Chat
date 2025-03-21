import socket
import threading
import time

BROADCAST_PORT = 50506
DISCOVERY_MSG = b"SECURE_CHAT_DISCOVERY"

def discover_peers():
    """Listens for new peers on the LAN."""
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    sock.bind(("", BROADCAST_PORT))

    while True:
        data, addr = sock.recvfrom(1024)
        if data == DISCOVERY_MSG:
            print(f"Discovered peer: {addr[0]}")
            yield addr[0]  # Return peer IP

def broadcast_presence():
    """Sends a broadcast packet to announce presence."""
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

    while True:
        sock.sendto(DISCOVERY_MSG, ("<broadcast>", BROADCAST_PORT))
        time.sleep(5)  # Send every 5 seconds

# Run discovery & broadcasting in background
threading.Thread(target=discover_peers, daemon=True).start()
threading.Thread(target=broadcast_presence, daemon=True).start()

import socket
import threading
import time

BROADCAST_PORT = 50000
DISCOVERY_MSG = b"HELLO_LAN_CHAT"

def broadcast_presence(port):
    """Broadcasts this peer's WebSocket port over UDP."""
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    message = f"{socket.gethostbyname(socket.gethostname())}:{port}".encode()
    
    while True:
        sock.sendto(message, ("<broadcast>", BROADCAST_PORT))
        time.sleep(5)  # Broadcast every 5 seconds

def listen_for_peers(peer_list):
    """Listens for UDP messages and updates peer list."""
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(("", BROADCAST_PORT))
    
    while True:
        data, addr = sock.recvfrom(1024)
        ip_port = data.decode()
        if ip_port not in peer_list:
            peer_list.append(ip_port)
            print(f"New peer discovered: {ip_port}")

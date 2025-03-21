from PyQt5.QtWidgets import QApplication, QMainWindow, QListWidget, QTextEdit, QVBoxLayout, QWidget, QHBoxLayout, QLineEdit, QPushButton, QFileDialog
from PyQt5.QtCore import QEventLoop
import asyncio
from ws_client import connect_to_peer

class JoinPage(QMainWindow):
    def __init__(self, peer_list):
        super().__init__()
        self.setWindowTitle("Join LAN Chat")
        self.setGeometry(200, 200, 400, 200)
        
        self.peer_list = peer_list
        self.layout = QVBoxLayout()
        
        self.name_input = QLineEdit(self)
        self.name_input.setPlaceholderText("Enter your name")
        
        self.join_button = QPushButton("Join Chat", self)
        self.join_button.clicked.connect(self.join_chat)
        
        self.layout.addWidget(self.name_input)
        self.layout.addWidget(self.join_button)
        
        container = QWidget()
        container.setLayout(self.layout)
        self.setCentralWidget(container)
        
    def join_chat(self):
        name = self.name_input.text()
        if name:
            self.hide()
            self.main_chat_window = MainChatWindow(name, self.peer_list)
            self.main_chat_window.show()

class MainChatWindow(QMainWindow):
    def __init__(self, username, peer_list):
        super().__init__()
        self.setWindowTitle(f"{username}'s Chat")
        self.setGeometry(200, 200, 600, 400)

        self.username = username
        self.peer_list = peer_list

        # Layout
        self.main_layout = QHBoxLayout()

        # Left: List of peers
        self.peer_list_widget = QListWidget()
        self.update_peer_list()

        # Right: Chat history and input
        self.chat_history = QTextEdit()
        self.chat_history.setReadOnly(True)

        self.input_box = QLineEdit(self)
        self.input_box.setPlaceholderText("Type a message...")

        self.send_button = QPushButton("Send", self)
        self.send_button.clicked.connect(self.send_message)

        self.file_button = QPushButton("Send File", self)
        self.file_button.clicked.connect(self.send_file)

        # Add widgets to layout
        self.right_layout = QVBoxLayout()
        self.right_layout.addWidget(self.chat_history)
        self.right_layout.addWidget(self.input_box)
        self.right_layout.addWidget(self.send_button)
        self.right_layout.addWidget(self.file_button)

        self.main_layout.addWidget(self.peer_list_widget)
        self.main_layout.addLayout(self.right_layout)

        container = QWidget()
        container.setLayout(self.main_layout)
        self.setCentralWidget(container)

        # Fix: Run async function properly
        self.run_async(self.connect_to_discovered_peers())

    def update_peer_list(self):
        """Updates the peer list UI."""
        self.peer_list_widget.clear()
        for peer in self.peer_list:
            self.peer_list_widget.addItem(peer)

    def run_async(self, coroutine):
        """Runs asyncio coroutine inside PyQt."""
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(coroutine)

    async def connect_to_discovered_peers(self):
        """Connects to all discovered peers."""
        for peer in self.peer_list:
            ip, port = peer.split(":")
            await connect_to_peer(ip, int(port))

    def send_message(self):
        message = self.input_box.text()
        if message:
            self.chat_history.append(f"{self.username}: {message}")
            self.input_box.clear()
            # Implement WebSocket message sending here

    def send_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select a file")
        if file_path:
            self.chat_history.append(f"Sending file: {file_path}")
            # Implement file sending logic here
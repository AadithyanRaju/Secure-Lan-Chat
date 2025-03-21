from PyQt5.QtWidgets import QApplication, QMainWindow, QListWidget, QTextEdit, QVBoxLayout, QWidget, QHBoxLayout, QLineEdit, QPushButton, QLabel, QFileDialog
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import Qt
import asyncio
from ws_client import connect_to_peer, send_message, send_file

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
        self.setGeometry(200, 200, 700, 500)

        self.username = username
        self.peer_list = peer_list

        # Layout Setup
        self.main_layout = QHBoxLayout()

        # Left Panel: Peer List
        self.peer_list_widget = QListWidget()
        self.peer_list_widget.setFixedWidth(200)
        self.peer_list_widget.setStyleSheet("background: #2C2F33; color: white; font-size: 16px; border-radius: 8px; padding: 4px;")
        self.update_peer_list()

        self.add_peer_button = QPushButton("➕ Add Peer")
        self.add_peer_button.setStyleSheet("background: #7289DA; color: white; font-weight: bold; border-radius: 5px; padding: 6px;")
        self.add_peer_button.clicked.connect(self.add_peer)

        left_layout = QVBoxLayout()
        left_layout.addWidget(QLabel("🔗 Online Peers"))
        left_layout.addWidget(self.peer_list_widget)
        left_layout.addWidget(self.add_peer_button)

        # Right Panel: Chat & Messages
        self.chat_history = QTextEdit()
        self.chat_history.setReadOnly(True)
        self.chat_history.setStyleSheet("background: #23272A; color: white; font-size: 14px; border-radius: 8px; padding: 4px;")

        self.input_box = QLineEdit(self)
        self.input_box.setPlaceholderText("Type a message...")
        self.input_box.setStyleSheet("padding: 8px; font-size: 14px; border-radius: 5px;")

        self.send_button = QPushButton("📩 Send")
        self.send_button.setStyleSheet("background: #43B581; color: white; font-weight: bold; border-radius: 5px; padding: 6px;")
        self.send_button.clicked.connect(self.send_message)

        self.file_button = QPushButton("📂 Send File")
        self.file_button.setStyleSheet("background: #FAA61A; color: white; font-weight: bold; border-radius: 5px; padding: 6px;")
        self.file_button.clicked.connect(self.send_file)

        right_layout = QVBoxLayout()
        right_layout.addWidget(QLabel(f"💬 Chat with {self.username}"))
        right_layout.addWidget(self.chat_history)
        right_layout.addWidget(self.input_box)
        
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.send_button)
        button_layout.addWidget(self.file_button)

        right_layout.addLayout(button_layout)

        # Combine Layouts
        self.main_layout.addLayout(left_layout)
        self.main_layout.addLayout(right_layout)

        container = QWidget()
        container.setLayout(self.main_layout)
        self.setCentralWidget(container)

        # Run async peer connection
        self.run_async(self.connect_to_discovered_peers())

    def update_peer_list(self):
        """Updates the peer list UI."""
        self.peer_list_widget.clear()
        for peer in self.peer_list:
            self.peer_list_widget.addItem(f"🟢 {peer}")

    def add_peer(self):
        """Allows user to manually add a new peer (Optional)."""
        peer_ip = self.input_box.text()
        if peer_ip:
            self.peer_list.append(peer_ip)
            self.update_peer_list()
            self.input_box.clear()

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
            peer_ip = self.peer_list_widget.currentItem().text()[2:]
            if peer_ip:
                asyncio.run(send_message(peer_ip, 50505, message))
                self.chat_history.append(f"🟢 You: {message}")
                self.input_box.clear()

    def send_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select a file")
        if file_path:
            peer_ip = self.peer_list_widget.currentItem().text()[2:]
            if peer_ip:
                asyncio.run(send_file(peer_ip, 50505, file_path))
                self.chat_history.append(f"📂 Sent file: {file_path.split('/')[-1]}")

# Run UI
if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    username = "User123"  # This should come from the join page
    peer_list = ["192.168.1.101:50505", "192.168.1.102:50505"]
    window = MainChatWindow(username, peer_list)
    window.show()
    sys.exit(app.exec_())
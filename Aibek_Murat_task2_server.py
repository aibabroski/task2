import socket
import threading
import hashlib
import os
import datetime

# ============ CONFIGURATIONS ============

HOST = '127.0.0.1'      # Listen on localhost
PORT = 8080            # Port to listen on

# Path to credentials file
CREDENTIALS_FILE = 'credentials.txt'
# Path to a log file for recording messages
LOG_FILE = 'server_log.txt'

# ========================================

def load_credentials():

    creds = {}
    if not os.path.exists(CREDENTIALS_FILE):
        # Create a default credentials file
        with open(CREDENTIALS_FILE, 'w') as f:
            user = 'aiba'
            password = '123'
            hashed = hashlib.sha256(password.encode()).hexdigest()
            f.write(f"{user}:{hashed}\n")

    with open(CREDENTIALS_FILE, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            user, stored_hash = line.split(":")
            creds[user] = stored_hash
    return creds


def verify_credentials(username, password, credentials):

    if username not in credentials:
        return False

    # Hash the incoming password and compare
    hashed_incoming = hashlib.sha256(password.encode()).hexdigest()
    return hashed_incoming == credentials[username]

class ChatServer:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clients = {}  # Map from (client_socket) -> username
        self.credentials = load_credentials()
        # Protect shared resources with a lock
        self.lock = threading.Lock()

    def start_server(self):
        # Bind and listen
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)  # accept up to 5 queued connections
        print(f"Server listening on {self.host}:{self.port}")

        # Continuously accept new clients
        while True:
            client_socket, addr = self.server_socket.accept()
            print(f"Connection from {addr}")

            # Start a thread to handle each client
            client_thread = threading.Thread(
                target=self.handle_client,
                args=(client_socket, addr)
            )
            client_thread.start()

    def handle_client(self, client_socket, addr):
        """
        1) Prompt for username/password
        2) Authenticate
        3) If successful, add to client list
        4) Receive messages and broadcast them
        """
        try:
            # Step 1: Prompt for username/password
            client_socket.send("Username: ".encode())
            username = client_socket.recv(1024).decode().strip()

            client_socket.send("Password: ".encode())
            password = client_socket.recv(1024).decode().strip()

            # Step 2: Verify credentials
            if not verify_credentials(username, password, self.credentials):
                client_socket.send("Authentication failed.\n".encode())
                client_socket.close()
                return  # End the thread here

            # If successful, notify client
            client_socket.send(f"Welcome, {username}!\n".encode())
            with self.lock:
                self.clients[client_socket] = username
            print(f"{username} authenticated successfully from {addr}")

            # Broadcast that user joined
            self.broadcast(f"{username} has joined the chat.", sender="Server")

            # Step 3: Continuously listen for messages from this client
            while True:
                data = client_socket.recv(1024)
                if not data:
                    # Client disconnected
                    break

                message = data.decode().strip()
                if message.lower() == "/quit":
                    # Client wants to disconnect
                    break

                # Broadcast the message to other clients
                full_msg = f"[{username}]: {message}"
                self.broadcast(full_msg, sender=username)

        except ConnectionResetError:
            # This happens if the client abruptly disconnects
            pass
        finally:
            # Cleanup when client disconnects
            with self.lock:
                user = self.clients.pop(client_socket, None)
            if user:
                self.broadcast(f"{user} has left the chat.", sender="Server")
                print(f"{user} from {addr} disconnected.")
            client_socket.close()

    def broadcast(self, message, sender="Server"):
        """
        Send `message` to all connected clients.
        Also log the message with a timestamp.
        """
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] {sender}: {message}\n"
        self.log_message(log_entry)

        with self.lock:
            for sock, user in self.clients.items():
                try:
                    sock.send((message + "\n").encode())
                except:
                    # If sending fails, ignore or remove client
                    pass

    def log_message(self, log_entry):
        """
        Write the given log_entry to LOG_FILE.
        """
        with open(LOG_FILE, 'a') as f:
            f.write(log_entry)


if __name__ == "__main__":
    chat_server = ChatServer(HOST, PORT)
    chat_server.start_server()

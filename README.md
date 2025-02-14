# Task 2: Multi-Client Chat Server

## Description
This project implements a **multi-client chat server** with **user authentication** using Python's `socket` and `threading` modules. The server allows multiple users to connect, authenticate, and send messages to each other in a shared chat room.

## Files
- **`Aibek_Murat_task2_server.py`** - Implements the chat server.
- **`Aibek_Murat_task2_client.py`** - Implements the chat client.
- **`credentials.txt`** - Stores user credentials (username: hashed_password).
- **`server_log.txt`** - Stores chat logs with timestamps.

## Features
- Multi-client support using threading.
- User authentication with **SHA-256** hashed passwords.
- Message broadcasting to all connected clients.
- Chat logging with timestamps.
- `/quit` command to leave the chat.

## Prerequisites
Ensure you have **Python 3.x** installed.

## How to Run

### Step 1: Start the Server
1. Open a terminal or command prompt.
2. Navigate to the directory containing `Aibek_Murat_task2_server.py`.
3. Run the following command:
   ```sh
   python Aibek_Murat_task2_server.py
   ```
4. The server will start listening on `127.0.0.1:8080`.

### Step 2: Start the Client(s)
1. Open another terminal.
2. Navigate to the directory containing `Aibek_Murat_task2_client.py`.
3. Run the following command:
   ```sh
   python Aibek_Murat_task2_client.py
   ```
4. Enter your **username** and **password**.
5. Start sending messages.

### Step 3: Using the Chat
- Once authenticated, type messages and press **Enter** to send.
- Type `/quit` to leave the chat.
- The server broadcasts messages to all connected clients.

## Expected Output
- **Server Output:**
  ```sh
  Server listening on 127.0.0.1:8080
  Connection from ('127.0.0.1', 54321)
  user1 authenticated successfully
  user1 has joined the chat.
  ```
- **Client Output:**
  ```sh
  Username: aiba
  Password: 123
  Welcome, aiba!
  [nurik]: Hello everyone!
  ```

## Notes
- Ensure `Aibek_Murat_task2_server.py` is running before starting any clients.
- Modify `credentials.txt` to add more users (format: `username:hashed_password`).
- The server maintains a log of all chat messages in `server_log.txt`.
- Clients will be disconnected if the server shuts down.


## Author
Aibek Murat

---


import socket
import threading
import sys

HOST = '127.0.0.1'    # The server's hostname or IP address
PORT = 8080         # The port used by the server

def receive_messages(client_socket):
    """ Continuously listen for messages from the server and print them. """
    while True:
        try:
            data = client_socket.recv(1024)
            if not data:
                print("Connection closed by the server.")
                break
            print(data.decode(), end="")  # end="" to avoid extra newlines
        except:
            # If there's any error in receiving, we consider the connection lost
            print("Disconnected from server.")
            break

    # Once disconnected, exit the program
    sys.exit(0)

def main():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((HOST, PORT))

    # Create a background thread to receive messages from the server
    thread = threading.Thread(target=receive_messages, args=(client_socket,))
    thread.daemon = True
    thread.start()

    try:
        while True:
            user_input = input()  # Wait for user to type something
            if user_input.strip().lower() == '/quit':
                client_socket.send(user_input.encode())
                break
            client_socket.send(user_input.encode())
    except KeyboardInterrupt:
        # If user hits Ctrl+C
        print("\nExiting...")

    client_socket.close()
    sys.exit(0)

if __name__ == "__main__":
    main()

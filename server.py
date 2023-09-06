import socket
import threading

HOST = 'localhost'
PORT = 5000

# Create the server socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# Bind the server socket to the host and port
server_socket.bind((HOST, PORT))

# Listen for incoming connections
server_socket.listen()

# Keep track of connected clients
clients = []

# Broadcast a message to all connected clients
def broadcast(message):
    for client in clients:
        client.send(message)

# Handle a client connection
def handle_client(client_socket, addr):
    print(f'New connection from {addr}')
    clients.append(client_socket)
    while True:
        try:
            # Receive data from the client
            data = client_socket.recv(1024)
            if data:
                # Broadcast the data to all other clients
                broadcast(data)
            else:
                # Remove the client from the list of connected clients
                clients.remove(client_socket)
                client_socket.close()
                print(f'{addr} disconnected')
                break
        except:
            # Remove the client from the list of connected clients
            clients.remove(client_socket)
            client_socket.close()
            print(f'{addr} disconnected')
            break

# Accept incoming connections and start a new thread for each client
while True:
    client_socket, addr = server_socket.accept()
    client_thread = threading.Thread(target=handle_client, args=(client_socket, addr))
    client_thread.daemon = True
    client_thread.start()

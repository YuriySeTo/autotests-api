import socket

HOST = "localhost"
PORT = 12345

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))

message = "Привет, сервер!"
client_socket.send(message.encode())


response = client_socket.recv(4096).decode()
print(response)

client_socket.close()
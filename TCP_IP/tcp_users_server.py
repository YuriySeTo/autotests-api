import socket
import threading

HOST = "localhost"
PORT = 12345

messages = []


def handle_client(client_socket, client_address):

    print(f"Пользователь с адресом: {client_address} подключился к серверу")

    try:
        while True:
            data = client_socket.recv(1024).decode()
            if not data:
                break

            print(f"Пользователь с адресом: {client_address} отправил сообщение: {data}")
            messages.append(data)


            response = "\n".join(messages)
            client_socket.send(response.encode())
    except ConnectionResetError:
        pass
    finally:
        client_socket.close()


def server():

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen(10)
    print(f"Сервер запущен на {HOST}:{PORT} и ждёт подключений...")

    while True:
        client_socket, client_address = server_socket.accept()
        thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
        thread.start()


if __name__ == "__main__":
    server()
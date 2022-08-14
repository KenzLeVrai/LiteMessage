import socket
import threading

HOST = '0.0.0.0'
PORT = 1234
LISTENER_LIMIT = 5
active_clients = []

def listen_for_messages(client, username):
    b = False
    while b == False:
        message = client.recv(2048).decode('utf-8')
        if message != '' and message != "disconnect":
            final_msg = username + '~' + message
            send_messages_to_all(final_msg)
        elif message == "disconnect":
            i = 0
            b = True
            for client_ in active_clients:
                if client_[0] == username:
                    active_clients.remove(client_)
                    client_[1].close()
                    break
                i += 1

def send_message_to_client(client, message):
    client.sendall(message.encode())

def send_messages_to_all(message):
    for user in active_clients:
        send_message_to_client(user[1], message)

def client_handler(client):
    while 1:
        username = client.recv(2048).decode('utf-8')
        if username != '':
            active_clients.append((username, client))
            prompt_message = "SERVER~" + f"{username} added to the chat"
            send_messages_to_all(prompt_message)
            break
    threading.Thread(target=listen_for_messages, args=(client, username, )).start()

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        server.bind((HOST, PORT))
        print(f"Running the server on {HOST} {PORT}")
    except:
        print(f"Unable to bind to host on {HOST} {PORT}")
    server.listen(LISTENER_LIMIT)
    while 1:
        client, address = server.accept()
        print(f'Client {address[0]}:{address[1]} successfully connected to the server')
        threading.Thread(target=client_handler, args=(client, )).start()

if __name__ == '__main__':
    main()
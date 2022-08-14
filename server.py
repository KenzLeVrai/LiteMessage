# Import required modules
import socket
import threading

HOST = '0.0.0.0'
PORT = 1234 # You can use any port between 0 to 65535
LISTENER_LIMIT = 5
active_clients = [] # List of all currently connected users

# Function to listen for upcoming messages from a client
def listen_for_messages(client, username):
    b = False
    while b == False:
        message = client.recv(2048).decode('utf-8')
        if message != '' and message != "disconnect":
            final_msg = username + '~' + message
            send_messages_to_all(final_msg)
        elif message == "disconnect":
            i = 0
            for client_ in active_clients:
                if client_[0] == username:
                    active_clients.remove(client_)
                    b = True
                    client_[1].close()
                    break
                i += 1


# Function to send message to a single client
def send_message_to_client(client, message):

    client.sendall(message.encode())

# Function to send any new message to all the clients that
# are currently connected to this server
def send_messages_to_all(message):
    
    for user in active_clients:
        send_message_to_client(user[1], message)

# Function to handle client
def client_handler(client):
    
    # Server will listen for client message that will
    # Contain the username
    while 1:

        username = client.recv(2048).decode('utf-8')
        if username != '':
            active_clients.append((username, client))
            prompt_message = "SERVER~" + f"{username} added to the chat"
            send_messages_to_all(prompt_message)
            break

    threading.Thread(target=listen_for_messages, args=(client, username, )).start()

# Main function
def main():

    # Creating the socket class object
    # AF_INET: we are going to use IPv4 addresses
    # SOCK_STREAM: we are using TCP packets for communication
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Creating a try catch block
    try:
        # Provide the server with an address in the form of
        # host IP and port
        server.bind((HOST, PORT))
        print(f"Running the server on {HOST} {PORT}")
    except:
        print(f"Unable to bind to host on {HOST} {PORT}")

    # Set server limit
    server.listen(LISTENER_LIMIT)

    # This while loop will keep listening to client connections
    while 1:

        client, address = server.accept()
        print(f'Client {address[0]}:{address[1]} successfully connected to the server')
        threading.Thread(target=client_handler, args=(client, )).start()


if __name__ == '__main__':
    main()
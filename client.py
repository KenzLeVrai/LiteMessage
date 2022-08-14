import socket
import sys
import threading
from time import sleep
import tkinter as tk
from tkinter import PhotoImage, scrolledtext
from tkinter import messagebox

DARK_GREY = '#121212'
MEDIUM_GREY = '#1F1B24'
OCEAN_BLUE = '#0A1751'
WHITE = "white"
FONT = ("Helvetica", 17)
BUTTON_FONT = ("Helvetica", 15)
SMALL_FONT = ("Helvetica", 13)

connected = False

# Creating a socket object
# AF_INET: we are going to use IPv4 addresses
# SOCK_STREAM: we are using TCP packets for communication
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def add_message(message):
    message_box.config(state=tk.NORMAL)
    message_box.insert(tk.END, message + '\n')
    message_box.config(state=tk.DISABLED)

def connect():
    global connected
    if connected:
        username = username_textbox.get()
        if username != '':
            client.sendall(username.encode())
            message_box.config(state=tk.NORMAL)
            message_button.config(state=tk.NORMAL)
            message_textbox.config(state=tk.NORMAL)
        else:
            messagebox.showerror("Invalid username", "Username cannot be empty")
    else:
        messagebox.showerror("Invalid server", "You're not connected to a server")

    threading.Thread(target=listen_for_messages_from_server, args=(client, )).start()

    username_textbox.config(state=tk.DISABLED)
    username_button.config(state=tk.DISABLED)

def send_message():
    global connected
    if connected:
        message = message_textbox.get()
        if message != '':
            client.sendall(message.encode())
            message_textbox.delete(0, len(message))
            if message == "disconnect":
                connected = False
                root.destroy()
                sys.exit()
        else:
            messagebox.showerror("Empty message", "Message cannot be empty")
    else:
        messagebox.showerror("Not connected", "Not connected to a server")

def on_close():
    global connected
    if connected:
        connected = False
        root.destroy()
        sleep(0.25)
        message = 'disconnect'
        client.sendall(message.encode())
        sleep(0.15)
    client.close()
    sys.exit()

def connect_to_server():
    global connected
    server = server_textbox.get()
    if connected == False:
        try:
            if server != "":
                if server == "default":
                    client.connect(('94.130.165.25', 25576))
                    add_message("[SERVER] Successfully connected to the server")
                    connected = True
                    server_textbox.config(state=tk.DISABLED)
                    server_button.config(state=tk.DISABLED)
                    username_textbox.config(state=tk.NORMAL)
                    username_button.config(state=tk.NORMAL)
                else:
                    server = server.split(":")
                    client.connect((server[0], int(server[1])))
                    add_message("[SERVER] Successfully connected to the server")
                    connected = True
                    server_textbox.config(state=tk.DISABLED)
                    server_button.config(state=tk.DISABLED)
                    username_textbox.config(state=tk.NORMAL)
                    username_button.config(state=tk.NORMAL)
        except:
            messagebox.showerror("Unable to connect to server", f"Unable to connect to server {server[0]}:{server[1]}")

root = tk.Tk()
img = PhotoImage(file='litemessage.png')
root.wm_iconphoto(True, img)
root.geometry("1150x600")
root.title("LiteMessage")
root.resizable(False, False)
root.protocol("WM_DELETE_WINDOW", on_close)

root.grid_rowconfigure(0, weight=1)
root.grid_rowconfigure(1, weight=4)
root.grid_rowconfigure(2, weight=1)

top_frame = tk.Frame(root, width=1150, height=100, bg=DARK_GREY)
top_frame.grid(row=0, column=0, sticky=tk.NSEW)

middle_frame = tk.Frame(root, width=1150, height=400, bg=MEDIUM_GREY)
middle_frame.grid(row=1, column=0, sticky=tk.NSEW)

bottom_frame = tk.Frame(root, width=1150, height=100, bg=DARK_GREY)
bottom_frame.grid(row=2, column=0, sticky=tk.NSEW)

server_label = tk.Label(top_frame, text="Host:port", font=FONT, bg=DARK_GREY, fg=WHITE)
server_label.pack(side=tk.LEFT, padx=10)

server_textbox = tk.Entry(top_frame, font=FONT, bg=MEDIUM_GREY, fg=WHITE, width=23, disabledforeground="#000000", insertbackground='white')
server_textbox.pack(side=tk.LEFT)

server_button = tk.Button(top_frame, text="Connect", font=BUTTON_FONT, bg=OCEAN_BLUE, fg=WHITE, command=connect_to_server, borderwidth=0, activebackground="#ffffff")
server_button.pack(side=tk.LEFT, padx=15)

username_label = tk.Label(top_frame, text="Enter username:", font=FONT, bg=DARK_GREY, fg=WHITE)
username_label.pack(side=tk.LEFT, padx=10)

username_textbox = tk.Entry(top_frame, font=FONT, bg=MEDIUM_GREY, fg=WHITE, width=23, disabledforeground="#000000", insertbackground='white')
username_textbox.pack(side=tk.LEFT)

username_button = tk.Button(top_frame, text="Join", font=BUTTON_FONT, bg=OCEAN_BLUE, fg=WHITE, command=connect, borderwidth=0, activebackground="#ffffff")
username_button.pack(side=tk.LEFT, padx=15)

message_textbox = tk.Entry(bottom_frame, font=FONT, bg=MEDIUM_GREY, fg=WHITE, width=38, disabledforeground="#000000", insertbackground='white')
message_textbox.pack(side=tk.LEFT, padx=10)

message_button = tk.Button(bottom_frame, text="Send", font=BUTTON_FONT, bg=OCEAN_BLUE, fg=WHITE, command=send_message, borderwidth=0, activebackground="#ffffff")
message_button.pack(side=tk.LEFT, padx=10)

message_box = scrolledtext.ScrolledText(middle_frame, font=SMALL_FONT, bg=MEDIUM_GREY, fg=WHITE, width=125, height=26.5)
message_box.config(state=tk.DISABLED)
message_box.pack(side=tk.LEFT)

message_box.config(state=tk.DISABLED)
message_button.config(state=tk.DISABLED)
message_textbox.config(state=tk.DISABLED)
username_textbox.config(state=tk.DISABLED)
username_button.config(state=tk.DISABLED)


def listen_for_messages_from_server(client):
    global connected
    while connected:

        message = client.recv(2048).decode('utf-8')
        if message != '':
            username = message.split("~")[0]
            content = message.split('~')[1]

            add_message(f"[{username}] {content}")

# main function
def main():

    root.mainloop()
    
if __name__ == '__main__':
    main()
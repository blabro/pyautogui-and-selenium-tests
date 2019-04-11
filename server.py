from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import time

clients = {}; addresses = {}
HOST = ''; PORT = 33000; BUFSIZ = 1024
ADDR = (HOST, PORT)
SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDR); saved_history = []

def accept_incoming_connections():
    """Sets up handling for incoming clients."""
    while True:
        client, client_address = SERVER.accept()
        print("%s:%s podłączony." % client_address)
        client.send(bytes("Hey! Podaj imię i kliknij enter!", "utf8") + bytes("\n", "utf8"))
        addresses[client] = client_address
        Thread(target=handle_client, args=(client,)).start()

def show_active(client):
    # shows active users
    users_list = list(clients.values())
    print('users_list: ', users_list)
    active_info = '\nAktywni: '
    client.send(bytes(active_info, "utf8") + bytes("\n", "utf8"))
    for x in users_list:
        client.send(bytes(x, "utf8") + bytes("\n", "utf8"))
    client.send(bytes("----------------------", "utf8") + bytes("\n", "utf8"))

def send_history(client, saved_history):
    for x in saved_history:
        client.send(x + bytes("\n", "utf8"))
        #client.send(b'00001010') #0x0A #+bytes('\r\n', "utf8") send(bytes(0x0A)): a@127.0.0.1: sd       a@127.0.0.1: df

def update_clients(clients, saved_history):
    for x in clients:
        print('x in update_clients:', x)
        show_active(x)
        send_history(x, saved_history)

def handle_client(client):  # Takes client socket as argument.
    """Handles a single client connection."""
    #print(client, ' ', client.recv(BUFSIZ).decode("utf8"), type(client))       #print(client.getsockname(), client.getpeername()[0])
    name = client.recv(BUFSIZ).decode("utf8") + '@' + client.getpeername()[0]
    clients[client] = name          #print(clients.values(), ' ', len(clients))
    welcome = 'Witaj %s! Prześlij {quit} lub zamknij aby wyjść. ' % name
    client.send(bytes(welcome, "utf8") + bytes("\n", "utf8"))
    #shows active users
    #show_active(client)
    #sending history to new client
    #send_history(client, saved_history)
    msg = "%s dołączył!" % name
    saved_history.append(bytes(msg, "utf8"))  # broadcast(bytes(msg, "utf8"))
    update_clients(clients, saved_history)

    while True:
        msg = client.recv(BUFSIZ)
        if msg != bytes("{quit}", "utf8"):
            saved_history.append(bytes(name + ': ', "utf8")+msg)
            print('saved_history: ', saved_history)
            broadcast(msg, name+": ")
        else:
            #broadcast(bytes("%s has left the chat." % name, "utf8"))
            saved_history.append(bytes("%s opuścił chat." % name, "utf8"))
            #client.send(bytes("{quit}", "utf8"))
            #time.sleep(1)
            client.close()
            del clients[client]
            update_clients(clients, saved_history)
            print("del clients[client]: ", clients)
            break


def broadcast(msg, prefix=""):  # prefix is for name identification.
    """Broadcasts a message to all the clients."""
    for sock in clients:
        sock.send(bytes(prefix, "utf8") + msg + bytes("\n", "utf8"))

if __name__ == "__main__":
    SERVER.listen(5)  # Listens for 5 connections at max.
    print("Waiting for connection...")
    ACCEPT_THREAD = Thread(target=accept_incoming_connections)
    ACCEPT_THREAD.start()  # Starts the infinite loop.
    ACCEPT_THREAD.join()
    SERVER.close()


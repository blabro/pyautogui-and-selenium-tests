from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import tkinter


def receive():
    """Handles receiving of messages."""
    while True:
        try:
            msg = client_socket.recv(BUFSIZ).decode("utf8")
            print(msg)
            if('Aktywni:' in msg):
                print('msg=="activenow"')
                msg_list.delete(3.0, tkinter.END)
            #elif('has left the chat' in msg):
            #    print('elif("has left the chat" in msg)')
            #    msg_list.delete(3.0, tkinter.END)
            msg_list.insert(tkinter.END, msg)
            msg_list.see(tkinter.END)
        except OSError:  # Possibly client has left the chat.
            break


def send(event=None):  # event is passed by binders. +
    """Handles sending of messages."""
    msg = my_msg.get()
    my_msg.set("")  # Clears input field.
    client_socket.send(bytes(msg, "utf8"))  # + bytes("\n", "utf8")
    if msg == "{quit}":
        client_socket.close()
        top.quit()


def delete(event=None):
    """Handles clear button"""
    msg_list.delete('1.0', tkinter.END)


def on_closing(event=None):
    """This function is to be called when the window is closed."""
    my_msg.set("{quit}")
    send()


top = tkinter.Tk()
top.title("connecto")

messages_frame = tkinter.Frame(top)
my_msg = tkinter.StringVar()  # For the messages to be sent.
my_msg.set("")
scrollbar = tkinter.Scrollbar(messages_frame)  # To navigate through past messages.

msg_list = tkinter.Text(messages_frame, height=15, width=50, yscrollcommand=scrollbar.set)
msg_list.pack(expand=1)
scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
msg_list.pack(side=tkinter.LEFT, fill=tkinter.BOTH)
msg_list.pack()

messages_frame.pack()


entry_field = tkinter.Entry(top, textvariable=my_msg)
entry_field.bind("<Return>", send)
entry_field.pack()
entry_field.focus()
send_button = tkinter.Button(top, text="Send", command=send)
send_button.pack(in_=top, side=tkinter.TOP)
clear_button = tkinter.Button(text="clear", command=delete)
clear_button.pack(in_=top, side=tkinter.LEFT)
top.protocol("WM_DELETE_WINDOW", on_closing)

HOST = '127.0.0.1'  # Default value.
PORT = False    # input('Give port name of press enter to get default')
if not PORT:
    PORT = 33000  # Default value.
else:
    PORT = int(PORT)
BUFSIZ = 1024
ADDR = (HOST, PORT)
client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect(ADDR)

receive_thread = Thread(target=receive)
receive_thread.start()
tkinter.mainloop()  # Starts GUI execution.

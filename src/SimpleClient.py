import sys
from socket import *
from threading import Thread

run = True


def receive(sockobj):
    global run
    while run:
        incoming = sockobj.recv(1024).decode("utf8")
        if incoming == "\\quit=success":
            run = False
        print(incoming)

serverHost = 'localhost'
serverPort = 8080

sockobj = socket(AF_INET, SOCK_STREAM) #IP,  TCP

try:
    sockobj.connect((serverHost, serverPort))
    print("Connected")
except OSError:
    print("Failed to connect")
    print(sys.exc_info())
    sys.exit()

listening_thread = Thread(target=receive, args=(sockobj, ))
listening_thread.start()

while run:
    print(run)
    sending = input()
    sockobj.send(bytes(sending, "utf8"))  # Send a message to the server

listening_thread.join(1)
sockobj.close()


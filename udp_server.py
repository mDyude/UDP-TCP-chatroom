import sys
import socket
import threading
import queue
import time

def run(serverSocket, serverPort):
    # The main server function.
    print("This is the server side. \nI am ready to receive connections on port " + str(serverPort))

    while True: 
        try:
            message, client_ip = serverSocket.recvfrom(2048)
            # if the message received is actually the nickname instead of the actual message
            # assign the name into the corresponding client list 
            if message.decode().startswith("Nickname:"):
                name = message.decode()[9:]
                clients[client_ip] = name
            
            elif message.decode().lower() == "!q" and clients[client_ip] != "":
                print("disconnecting.")
                handleDisconnet(client_ip)

            #  if the received message is an actuale msg
            #  put it into the queue
            else:
                messages.put((message, client_ip))
        except Exception as e:
            print(e)

def broadcast():
    while True:
        message, client_ip = messages.get()
        print(clients)
        print(f"{message.decode()}")
        for client, name in clients.items():
            # if client != client_ip:
            try:
                if message.decode().lower() == "!q":
                    handleDisconnet(client)
                else:
                    broadcastMessage = f"{clients[client_ip]}: {message.decode()}"
                    serverSocket.sendto(broadcastMessage.encode(), client)
            except Exception as e:
                handleDisconnet(client)
                print(e)


def handleDisconnet(client):
    try:
        print(f"Removing client: {clients[client]}")
        del clients[client]
    except KeyError:
        pass
    except Exception as e:
        print(e)


# **Main Code**:  
if __name__ == "__main__":
    # considering how UDP works, it's better to securely transmit the messages by putting it in a list
    messages = queue.Queue()
    clients = {}
    server_ip = "127.0.0.1"
    server_port = 9321
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # Creating a UDP socket.\
    serverSocket.bind((server_ip, server_port))

    threading.Thread(target=broadcast, daemon=True).start()

    run(serverSocket, server_port)  # Calling the function to start the server.

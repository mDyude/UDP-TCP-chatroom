import sys
import socket
import threading
from datetime import datetime

def handleClient(connectionSocket):
    while True:
        try: 
            message = connectionSocket.recv(2048).decode()
            if message.lower() == "!q":
                handleDisconnect(connectionSocket)
            else:
                # print("before broadcasting message")
                broadcast(connectionSocket, message)
                # print the server ip and the thread id
                print(f"Message received from '{server_ip}', {threading.get_ident()} joining: {clientNames[clients.index(connectionSocket)]} {current_time}")
                print(f"the message is {message}")
        except Exception as e:
            handleDisconnect(connectionSocket)
            # print(e)
            break
    
    connectionSocket.close()

# broadcast mesages to all the clients
def broadcast(connectionSocket, message):
    try:
        for client in clients:
            # print("broadcasting a message " + current_time)
            client.send(f"{clientNames[clients.index(connectionSocket)]}: {message}".encode())
    except:
        handleDisconnect(connectionSocket),

# how the server handles diconnection
def handleDisconnect(connectionSocket):
    try:
        print("Disconnect from the client " + current_time)
        index = clients.index(connectionSocket)
        clients.remove(connectionSocket)
        connectionSocket.close()
        clientName = clientNames[index]
        
        broadcast(connectionSocket, f"{clientName} has left the chat. " + current_time)
        clientNames.remove(clientName)
    except:
        pass


def run(server):
    while True:
        try:
            connectionSocket, addr = server.accept()
            # print("Connected. Address is: " + addr)
            
            # first receive the client name from the client end 
            clientName = connectionSocket.recv(2048).decode()
            clientNames.append(clientName)
            clients.append(connectionSocket)
            print("Client " + clientName + " connected. " + current_time)
            print(clientNames)
            # broadcast(connectionSocket, f"{clientName} joined the chat. " + current_time)
            
            thread = threading.Thread(target=handleClient, args=(connectionSocket,), daemon=True)
            thread.start()
        
        except Exception as e:
            handleDisconnect(connectionSocket)
            # print(e)
            break

    server.close()
    print('Server closed')


# **Main Code**:  
if __name__ == "__main__":
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")

    clients = []
    clientNames = []
    server_ip = "127.0.0.1"
    server_port = 9321
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)# Creating a TCP socket.
    server_socket.bind((server_ip, server_port))
    server_socket.listen(3) # size of the waiting_queue that stores the incoming requests to connect.
    print("This is the server side. \nI am ready to receive connections on port " + str(server_port))

    run(server_socket)# Calling the function to start the server.

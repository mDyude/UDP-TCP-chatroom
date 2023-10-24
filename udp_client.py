import socket
import threading
import argparse
import sys
import os

def run(clientSocket, serverAddr, serverPort):
    print("Chatroom entered. !q to exit.")
    try:
        while True:
            message = input()
            if message.lower() == "!q":
                clientSocket.sendto(message.encode(), (serverAddr, serverPort))

                print("You have been disconnected from the server.")
                # print("Now you can safely use CTRL + C to exit.")
                sys.exit(0)
                

            else:
            # then send the actual message
                clientSocket.sendto(message.encode(), (serverAddr, serverPort))
    except:
        pass

def receive(clientSocket):
    while True:
        try: 
            message, addr = clientSocket.recvfrom(2048)
            # print("msg received")
            print(message.decode())
        except Exception as e:
            # print(e)
            pass

# **Main Code**:  
if __name__ == "__main__":
    try: 
        if len(sys.argv) != 2:
            print("Only one argument (your nickname) will be accepted. ")
        else:
            parser = argparse.ArgumentParser(description='Argument Parser')
            parser.add_argument('name')  # to use: python tcp_client.py username
            args = parser.parse_args()
            client_name = args.name
            server_addr = '127.0.0.1'
            server_port = 9321

    
            clientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
            #  first send the nickname to the server 
            clientSocket.sendto(f"Nickname:{client_name}".encode(), (server_addr, server_port))
            # daemon is set to true in order to true, so that the thread/program will shut down neatly
            threading.Thread(target=receive, args=(clientSocket, ), daemon=True).start()

            run(clientSocket, server_addr, server_port)  # Calling the function to start the client.

    except Exception as e:
        # print(e)
        pass

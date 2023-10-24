import sys
import socket
import threading
import argparse
from datetime import datetime

def run(clientSocket, clientname):
    print("Chatroom entered. !q to exit.")
    try:
        # prompt for input messages
        while True:
            # print("running " + current_time)
            # print(f"{clientname}", end = "", flush = True)
            message = input()
            clientSocket.send(message.encode())
            if message.lower() == "!q":
                print("You have been disconnected from the server.")
                sys.exit(0)
            
            # receive(clientSocket)

    except Exception as e:
        clientSocket.close()
        print(e)
        

# receive messages 
def receive(clientSocket):
    while True: 
        try:
            # print("receiving a msg " + current_time)
            rcvMsg = clientSocket.recv(2048).decode()
            print(rcvMsg)
        except Exception as e:
            print(e)
            clientSocket.close()
            print("Connection closed. From receive() " + current_time)
            break
            

# **Main Code**:  
if __name__ == "__main__":
    try: 
        if len(sys.argv) != 2:
            print("Only one argument (your nickname) will be accepted. ")
        else:
            now = datetime.now()
            current_time = now.strftime("%H:%M:%S")

            parser = argparse.ArgumentParser(description='Argument Parser')
            parser.add_argument('name')  # to use: python tcp_client.py username
            args = parser.parse_args()
            client_name = args.name
            server_addr = '127.0.0.1'
            server_port = 9321

            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #TCP
            client_socket.connect((server_addr, server_port))

            # first send the current client name to the server
            client_socket.send(client_name.encode())

            # run(client_socket, client_name)
            run_thread = threading.Thread(target=run, args=(client_socket, client_name, ))
            run_thread.daemon = True
            run_thread.start()
            receive_thread = threading.Thread(target=receive, args=(client_socket, ))
            receive_thread.daemon = True
            receive_thread.start()
            # telling the main thread to wait until run_thread is completed
            run_thread.join()

            
    except Exception as e:
        print(e)

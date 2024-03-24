import socket
import threading
from game import Game 

g = Game(5)

def handleclient(clientsocket):
    while True:
        # Receive data from the client
        data = clientsocket.recv(1024)
        if not data:
            break

        # Decode the received message
        message = data.decode('utf-8')

        delim = ' '
        print(message)
        lastspace = message.rfind(' ')
        word = message[lastspace + 1:]
        print('actual input:',word)
        if word in g.mem: 
            print('not unique')
        else:
            g.add_word(word)
        # Check if the client wants to quit
        if message.lower() == 'quit':
            break

    # Close the client connection when done
    clientsocket.close()

def main():
    # Set up the server socket
    server_host = '0.0.0.0'  # Listen on all network interfaces
    server_port = 5555  # Choose any available port
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((server_host, server_port))
    server_socket.listen(5)  # Listen for incoming connections

    print("Server listening on {}:{}".format(server_host, server_port))

    try:
        while True:
            # Accept incoming connections
            client_socket, client_address = server_socket.accept()
            print("Accepted connection from:", client_address)

            # Create a new thread to handle the client
            client_thread = threading.Thread(target=handleclient, args=(client_socket,))
            client_thread.start()

    except KeyboardInterrupt:
        print("Server shutting down...")
        # TODO: join client threads back to main
        client_thread.join()
        server_socket.close()



if __name__ == "__main__":
    main()
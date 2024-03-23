import dictionary
import socket
import threading

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
            client_thread = threading.Thread(target=handle_client, args=(client_socket,))
            client_thread.start()

    except KeyboardInterrupt:
        print("Server shutting down...")
        server_socket.close()

if __name__ == "__main":
    main()
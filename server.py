import socket
import threading
import dictionary

api_key = '57300dd3-e1ec-43cb-81fd-5b44fdf7df7d'

# Function to handle client connections
def handle_client(client_socket):
    while True:
        # Receive data from the client
        data = client_socket.recv(1024)
        if not data:
            break

        # Decode the received message
        message = data.decode("utf-8")
        print("Received:", message)

        # Check if the client wants to quit
        if message.lower() == "quit":
            break
        if(dictionary.is_valid_word(message, api_key)):
            print("This is a valid word")
        else:
            print("This is not a valid word")
        
    # Close the client connection when done
    client_socket.close()

# Main function to set up the server
def main():
    # Set up the server socket
    server_host = "0.0.0.0"  # Listen on all network interfaces
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
            client_thread = threading.Thread(
                target=handle_client, args=(client_socket,)
            )
            client_thread.start()

    except KeyboardInterrupt:
        print("Server shutting down...")
        server_socket.close()


if __name__ == "__main__":
    main()

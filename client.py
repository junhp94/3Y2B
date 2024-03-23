def handleclient(clientsocket):
    while True:
        # Receive data from the client
        data = clientsocket.recv(1024)
        if not data:
            break

        # Decode the received message
        message = data.decode('utf-8')
        print("Received:", message)

        # Check if the client wants to quit
        if message.lower() == 'quit':
            break

    # Close the client connection when done
    clientsocket.close()

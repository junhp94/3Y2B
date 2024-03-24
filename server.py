import socket
import threading
import dictionary

api_key = '57300dd3-e1ec-43cb-81fd-5b44fdf7df7d'

from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_socketio import SocketIO, emit

app = Flask(__name__)
CORS(app)
socketio = SocketIO(app)

messages = []  # Store messages received from players
current_players = []


@app.route("/", methods=["POST"])
def handle_message():
    data = request.json
    player_id = data.get("playerId", "")
    voice_input = data.get("voiceInput", "")

    print(f"Current players :  {current_players}")
    print(f"Received from Player {player_id}: {voice_input}")

    message = {"playerId": player_id, "voiceInput": voice_input}
    messages.append(message)  # Store the message
    socketio.emit("message", message)  # Send the message to all clients
    return jsonify({"status": "success"})


@app.route("/adduser", methods=["POST"])
def adduser():
    player_id = request.json.get("playerId")
    if player_id:
        current_players.append(player_id)
        print(f"Current players :  {current_players}")
        return jsonify({"message": "User added successfully"})
    else:
        return jsonify({"error": "Player ID is required"}), 400


@app.route("/deleteuser", methods=["POST"])
def deleteuser():
    player_id = request.json.get("playerId")
    if player_id:
        current_players.remove(player_id)
        print(f"Current players :  {current_players}")
        return jsonify({"message": "User deleted successfully"})
    else:
        return jsonify({"error": "Player ID is required"}), 400


@app.route("/current_users")
def get_current_users():
    return jsonify({"current_users": current_players})


if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=5555)

# # Function to handle client connections
# def handle_client(client_socket):
#     while True:
#         # Receive data from the client
#         data = client_socket.recv(1024)
#         if not data:
#             break

#         # print(data)

#         # Decode the received message
#         message = data.decode("utf-8")
#         print("Received:", message)

#         # Check if the client wants to quit
#         if message.lower() == "quit":
#             break

#         # if(dictionary.is_valid_word(message, api_key)):
#         #     print("This is a valid word")
#         # else:
#         #     print("This is not a valid word")
        
#     # Close the client connection when done
#     client_socket.close()

# # Main function to set up the server
# def main():
#     # Set up the server socket
#     server_host = "0.0.0.0"  # Listen on all network interfaces
#     server_port = 5555  # Choose any available port
#     server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     server_socket.bind((server_host, server_port))
#     server_socket.listen(5)  # Listen for incoming connections

#     # print("Server listening on {}:{}".format(server_host, server_port))

#     try:
#         while True:
#             # Accept incoming connections
#             client_socket, client_address = server_socket.accept()
#             # print("Accepted connection from:", client_address)

#             # Create a new thread to handle the client
#             client_thread = threading.Thread(
#                 target=handle_client, args=(client_socket,)
#             )
#             client_thread.start()

#     except KeyboardInterrupt:
#         # print("Server shutting down...")
#         server_socket.close()


# if __name__ == "__main__":
#     main()

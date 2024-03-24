
import logging

from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_socketio import SocketIO, emit

app = Flask(__name__)
CORS(app)
socketio = SocketIO(app)


# Set the logging level to ignore requests to the `/current_users` endpoint
logging.getLogger("werkzeug").setLevel(logging.ERROR)

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


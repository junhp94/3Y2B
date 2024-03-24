from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_socketio import SocketIO, emit

app = Flask(__name__)
CORS(app)
socketio = SocketIO(app)

messages = []  # Store messages received from players


@app.route("/", methods=["POST"])
def handle_message():
    data = request.json
    player_id = data.get("playerId", "")
    voice_input = data.get("voiceInput", "")
    print(f"Received from Player {player_id}: {voice_input}")
    message = {"playerId": player_id, "voiceInput": voice_input}
    messages.append(message)  # Store the message
    socketio.emit("message", message)  # Send the message to all clients
    return jsonify({"status": "success"})


if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=5555)

import logging
import random
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
current_turn = None
current_letter = None


def initialize_game():
    global current_turn
    global current_letter
    current_turn = random.choice(current_players)
    current_letter = random.choice("abcdefghijklmnopqrstuvwxyz").upper()
    print(
        f"Starting game with current turn: {current_turn}, current letter: {current_letter}"
    )
    return jsonify({"Current letter : {current_letter}"})


def get_next_turn():
    current_index = current_players.index(current_turn)
    next_index = (current_index + 1) % len(current_players)
    return current_players[next_index]


@app.route("/", methods=["POST"])
def handle_message():
    global current_turn
    global current_letter

    data = request.json
    player_id = data.get("playerId", "")
    voice_input = data.get("voiceInput", "")

    if player_id == current_turn:
        if voice_input.startswith(current_letter):
            print(f"Current players :  {current_players}")
            print(f"Received from Player {player_id}: {voice_input}")

            message = {"playerId": player_id, "voiceInput": voice_input}
            messages.append(message)  # Store the message
            socketio.emit("message", message)  # Send the message to all clients
            current_turn = get_next_turn()
            emit(
                "turn_update", {"currentTurn": current_turn}
            )  # Send turn update to client
            return jsonify({"status": "success"})
        else:
            return (
                jsonify(
                    {
                        "error": f"Your message must start with the letter '{current_letter}'. Try again."
                    }
                ),
                400,
            )
    else:
        return jsonify({"error": "It's {current_turn}'s turn to send a message."}), 400


@app.route("/adduser", methods=["POST"])
def adduser():
    player_id = request.json.get("playerId")
    if player_id:
        current_players.append(player_id)
        print(f"Current players :  {current_players}")
        if len(current_players) == 1:
            initialize_game()
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


@app.route("/current_letter")
def get_current_letter():
    return jsonify({"current_letter": current_letter})


if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=5555)

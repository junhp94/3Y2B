from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

members_list = ["member 1", "member 2", "member 3"]

@app.route("/member")
def get_members():
    return jsonify({"members": members_list})

@app.route("/add_member", methods=["POST"])
def add_member():
    data = request.json
    new_member = data.get("username")
    if new_member:
        members_list.append(new_member)
        return jsonify({"message": "Member added successfully", "members": members_list})
    else:
        return jsonify({"error": "Username not provided"}), 400

if __name__ == "__main__":
    app.run(debug=True)
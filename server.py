from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

# ===== CONFIG =====
SWARMNODE_API_KEY = "1a032cd4a51c4264aa47da33e05e76d6"
AGENT_ID = "f40d1956-56f0-4ed6-b18a-ffdf08e80d55"
# ==================

@app.route("/typeform", methods=["POST"])
def handle_typeform():
    data = request.json
    print("Received Typeform payload")

    payload = {
        "typeform_response": data
    }

    headers = {
        "Authorization": f"Bearer {SWARMNODE_API_KEY}",
        "Content-Type": "application/json"
    }

    url = f"https://api.swarmnode.com/v1/agents/{AGENT_ID}/input"

    response = requests.post(url, headers=headers, json=payload)

    print("SwarmNode status:", response.status_code)
    print("SwarmNode response:", response.text)

    return jsonify({"status": "ok"}), 200


@app.route("/", methods=["GET"])
def health_check():
    return "Server is running", 200


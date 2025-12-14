from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

SWARMNODE_API_KEY = os.getenv("SWARMNODE_API_KEY")
SWARMNODE_AGENT_ID = os.getenv("SWARMNODE_AGENT_ID")

@app.route("/typeform", methods=["POST"])
def handle_typeform():
    data = request.json

    if not SWARMNODE_API_KEY or not SWARMNODE_AGENT_ID:
        return jsonify({"error": "Missing SwarmNode config"}), 500

    url = f"https://api.swarmnode.com/v1/agents/{SWARMNODE_AGENT_ID}/input"

    headers = {
        "Authorization": f"Bearer {SWARMNODE_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "input": data
    }

    response = requests.post(url, json=payload, headers=headers)

    return jsonify({
        "status": "sent_to_swarmnode",
        "swarmnode_status": response.status_code,
        "swarmnode_response": response.text
    }), 200

from flask import Flask, request, jsonify
import requests
import os
import logging

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

AGENT_ID = os.environ.get("SWARMNODE_AGENT_ID")
SWARMNODE_API_KEY = os.environ.get("SWARMNODE_API_KEY")

@app.route("/")
def home():
    return "Webhook server is running", 200

@app.route("/typeform", methods=["POST"])
def handle_typeform():
    data = request.json
    logging.info(f"Received Typeform payload: {data}")

    payload = {"input": data}
    url = f"https://api.swarmnode.com/v1/agents/{AGENT_ID}/input"
    headers = {
        "Authorization": f"Bearer {SWARMNODE_API_KEY}",
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        logging.info(f"Sent to SwarmNode: {url} with payload={payload}")
        return jsonify({"status": "success", "swarmnode_response": response.json()}), 200
    except Exception as e:
        logging.error(f"Request error: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)


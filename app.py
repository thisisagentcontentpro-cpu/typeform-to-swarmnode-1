import os
import requests
from flask import Flask, request, jsonify
import logging

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

# Get your SwarmNode agent ID and API key from environment variables
AGENT_ID = os.environ.get("f40d1956-56f0-4ed6-b18a-ffdf08e80d55")  # Must match Render environment variable name
API_KEY = os.environ.get("1a032cd4a51c4264aa47da33e05e76d6")    # Must match Render environment variable name

SWARMNODE_ENDPOINT = f"https://api.swarmnode.com/v1/agents/{AGENT_ID}/input"

@app.route("/typeform", methods=["POST"])
def typeform_webhook():
    try:
        payload = request.json
        logging.info(f"Received Typeform payload: {payload}")

        # Prepare the data for SwarmNode
        data = {
            "input": payload
        }

        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        }

        # Send data to SwarmNode agent
        response = requests.post(SWARMNODE_ENDPOINT, json=data, headers=headers)
        response.raise_for_status()
        logging.info(f"SwarmNode response: {response.json()}")

        return jsonify({"status": "success"}), 200

    except requests.exceptions.RequestException as e:
        logging.error(f"Request error: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == "__main__":
    # Use 0.0.0.0 for Render to expose the server externally
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)



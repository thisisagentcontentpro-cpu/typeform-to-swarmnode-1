from flask import Flask, request, jsonify
import requests
import os

# Initialize Flask app
app = Flask(__name__)

# Get API key and agent ID from environment variables
SWARMNODE_API_KEY = os.getenv("SWARMNODE_API_KEY")
AGENT_ID = os.getenv("AGENT_ID")

# Test endpoint to make sure the service is running
@app.route("/test", methods=["GET"])
def test():
    return jsonify({"status": "success"}), 200

# Typeform webhook endpoint
@app.route("/typeform", methods=["POST"])
def handle_typeform():
    data = request.json
    print("Received data from Typeform:", data)  # DEBUG: check logs in Render

    payload = {"input": data}
    url = f"https://api.swarmnode.com/v1/agents/{AGENT_ID}/input"
    headers = {
        "Authorization": f"Bearer {SWARMNODE_API_KEY}",
        "Content-Type": "application/json"
    }

    try:
        # Skip SSL verification temporarily to prevent TLS errors
        response = requests.post(url, json=payload, headers=headers, verify=False)
        print("SwarmNode response:", response.text)  # DEBUG: check logs
        return jsonify({
            "status": "success",
            "swarmnode_response": response.json()
        }), 200

    except Exception as e:
        print("Error sending to SwarmNode:", e)  # DEBUG: check logs
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

# Run locally (Render ignores this)
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)

from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

# Replace with your actual API key and Agent ID
SWARMNODE_API_KEY = "1a032cd4a51c4264aa47da33e05e76d6"
AGENT_ID = "f40d1956-56f0-4ed6-b18a-ffdf08e80d55"

@app.route("/typeform", methods=["POST"])
def handle_typeform():
    try:
        # Receive JSON from Typeform webhook
        data = request.json

        # Optional: Extract only the answers if you want
        answers = data.get("form_response", {}).get("answers", [])

        # Build payload for SwarmNode
        payload = {
            "input": {
                "typeform_data": data,
                "answers": answers
            }
        }

        # SwarmNode API URL
        url = f"https://api.swarmnode.com/v1/agents/{AGENT_ID}/input"
        headers = {
            "Authorization": f"Bearer {SWARMNODE_API_KEY}",
            "Content-Type": "application/json"
        }

        # Send to SwarmNode
        response = requests.post(url, json=payload, headers=headers)

        # Return success with SwarmNode response
        return jsonify({
            "status": "success",
            "swarmnode_response": response.json()
        }), 200

    except Exception as e:
        # Return error with exception details
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

# Optional: simple root route to verify server is live
@app.route("/", methods=["GET"])
def home():
    return "Server is live!", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))

from flask import Flask, request, jsonify
import requests

# Replace these with your actual SwarmNode API Key and Agent ID
SWARMNODE_API_KEY = "1a032cd4a51c4264aa47da33e05e76d6"
AGENT_ID = "f40d1956-56f0-4ed6-b18a-ffdf08e80d55"

app = Flask(__name__)

@app.route("/")
def index():
    return "Server is running", 200

@app.route("/typeform", methods=["POST"])
def handle_typeform():
    data = request.json

    payload = {"input": data}

    url = f"https://api.swarmnode.com/v1/agents/{AGENT_ID}/input"
    headers = {
        "Authorization": f"Bearer {SWARMNODE_API_KEY}",
        "Content-Type": "application/json"
    }

    try:
        # verify=False disables SSL verification to avoid TLS errors
        response = requests.post(url, json=payload, headers=headers, verify=False)
        return jsonify({
            "status": "success",
            "swarmnode_response": response.json()
        }), 200

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

if __name__ == "__main__":
    # Use port 10000 because Render detects it automatically
    app.run(host="0.0.0.0", port=10000)


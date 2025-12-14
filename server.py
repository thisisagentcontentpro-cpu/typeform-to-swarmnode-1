from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

AGENT_ID = "f40d1956-56f0-4ed6-b18a-ffdf08e80d55"
SWARMNODE_API_KEY = "1a032cd4a51c4264aa47da33e05e76d6"

# Typeform webhook handler
@app.route("/typeform", methods=["POST"])
def handle_typeform():
    data = request.json
    payload = {"input": data}

    url = f"https://api.swarmnode.com/v1/agents/AGENT_ID/input"
    headers = {
        "Authorization": f"Bearer SWARMNODE_API_KEY",
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(url, json=payload, headers=headers, verify=False)
        return jsonify({
            "status": "success",
            "swarmnode_response": response.text,
            "http_status": response.status_code
        })
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

# Test endpoint to confirm SwarmNode connection
@app.route("/test", methods=["GET"])
def test_swarmnode():
    payload = {"input": {"test": "hello"}}
    url = f"https://api.swarmnode.com/v1/agents/AGENT_ID/input"
    headers = {
        "Authorization": f"Bearer SWARMNODE_API_KEY",
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(url, json=payload, headers=headers, verify=False)
        return jsonify({
            "status": "success",
            "swarmnode_response": response.text,
            "http_status": response.status_code
        })
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)


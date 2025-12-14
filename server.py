from flask import Flask, request, jsonify
import requests
import os
import traceback

app = Flask(__name__)

# Get your credentials from environment variables
AGENT_ID = os.getenv("f40d1956-56f0-4ed6-b18a-ffdf08e80d55")
SWARMNODE_API_KEY = os.getenv("1a032cd4a51c4264aa47da33e05e76d6")

@app.route("/", methods=["GET"])
def home():
    return "Server is running!", 200

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
        # Disable SSL verification for testing
        response = requests.post(url, json=payload, headers=headers, verify=False)
        return jsonify({
            "status": "success",
            "swarmnode_response": response.json()
        }), 200
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e),
            "trace": traceback.format_exc()
        }), 500

if __name__ == "__main__":
    # Use the port Render sets
    import os
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)


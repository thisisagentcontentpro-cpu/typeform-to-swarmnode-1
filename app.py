from flask import Flask, request, jsonify
import os
import requests

app = Flask(__name__)

# Your SwarmNode Agent ID and API Key from environment variables
AGENT_ID = os.environ.get("f40d1956-56f0-4ed6-b18a-ffdf08e80d55")
API_KEY = os.environ.get("1a032cd4a51c4264aa47da33e05e76d6")

# ===== Homepage route =====
@app.route("/", methods=["GET"])
def home():
    return "✅ Typeform to SwarmNode app is running!", 200

# ===== Typeform webhook route =====
@app.route("/typeform", methods=["POST"])
def typeform_webhook():
    payload = request.json
    print("INFO: Received Typeform payload:", payload)

    # Example: send data to SwarmNode
    url = f"https://api.swarmnode.com/v1/agents/{AGENT_ID}/input"
    headers = {"Authorization": f"Bearer {API_KEY}"}

    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        return jsonify({"status": "success"}), 200
    except requests.exceptions.RequestException as e:
        print("ERROR: Request error:", e)
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)


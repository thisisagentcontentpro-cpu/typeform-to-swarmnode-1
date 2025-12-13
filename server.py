from flask import Flask, request, jsonify
import requests

app = Flask(__name__)  # Must be 'app'

SWARMNODE_API_KEY = "1a032cd4a51c4264aa47da33e05e76d6"
AGENT_ID = "YOUR_AGENT_ID"

@app.route("/", methods=["POST"])
def webhook():
    data = request.json

    # Extract fields from Typeform submission
    full_name = data.get("full_name", "")
    email = data.get("email", "")
    plan = data.get("plan", "")
    city = data.get("city", "")
    niche = data.get("niche", "")

    # Send data to SwarmNode agent
    payload = {
        "full_name": full_name,
        "email": email,
        "plan": plan,
        "city": city,
        "niche": niche
    }

    headers = {
        "Authorization": f"Bearer {1a032cd4a51c4264aa47da33e05e76d6}",
        "Content-Type": "application/json"
    }

    url = f"https://api.swarmnode.com/v1/agents/{f40d1956-56f0-4ed6-b18a-ffdf08e80d55}/input"
    response = requests.post(url, headers=headers, json=payload)

    return jsonify({"status": "sent", "swarmnode_status": response.status_code})

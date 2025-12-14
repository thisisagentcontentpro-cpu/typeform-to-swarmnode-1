from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

# ====== CONFIG ======
SWARMNODE_API_KEY = "sk-1a032cd4a51c4264aa47da33e05e76d6"  # Replace with your SwarmNode API key
SWARMNODE_AGENT_ID = "f40d1956-56f0-4ed6-b18a-ffdf08e80d55"   # Replace with your Agent ID
SWARMNODE_URL = f"https://api.swarmnode.com/v1/agents/{SWARMNODE_AGENT_ID}/input"

# ====== ROUTE ======
@app.route("/typeform-webhook", methods=["POST"])
def typeform_webhook():
    data = request.json  # JSON payload from Typeform
    
    # Extract data from Typeform payload (example field names)
    full_name = data.get("full_name", "")
    email = data.get("email", "")
    plan = data.get("plan", "Starter")
    city = data.get("city", "")
    niche = data.get("niche", "")
    
    # Construct payload for SwarmNode agent
    agent_payload = {
        "full_name": full_name,
        "email": email,
        "plan": plan,
        "city": city,
        "niche": niche
    }
    
    headers = {
        "Authorization": f"Bearer {SWARMNODE_API_KEY}",
        "Content-Type": "application/json"
    }
    
    # Send data to SwarmNode agent
    response = requests.post(SWARMNODE_URL, json=agent_payload, headers=headers)
    
    if response.status_code == 200:
        return jsonify({"status": "success", "swarmnode_response": response.json()}), 200
    else:
        return jsonify({"status": "error", "message": response.text}), 500

# ====== MAIN ======
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)


from flask import Flask, request, jsonify
import requests
import json

app = Flask(__name__)

# ====== CONFIG ======
SWARMNODE_API_KEY = "1a032cd4a51c4264aa47da33e05e76d6"
AGENT_ID = "f40d1956-56f0-4ed6-b18a-ffdf08e80d55"
# ===================

@app.route("/", methods=["POST"])
def typeform_to_swarmnode():
    try:
        # Get JSON payload from Typeform webhook
        data = request.get_json()
        
        # Example: Typeform answers mapping
        # Adjust field names according to your Typeform questions
        payload = {
            "full_name": data.get("full_name", ""),
            "email": data.get("email", ""),
            "plan": data.get("plan", ""),
            "city": data.get("city", ""),
            "niche": data.get("niche", ""),
            "timestamp": data.get("timestamp", "")
        }

        # Send to SwarmNode
        url = f"https://api.swarmnode.com/v1/agents/{f40d1956-56f0-4ed6-b18a-ffdf08e80d55}/input"
        headers = {
            "Authorization": "Bearer 1a032cd4a51c4264aa47da33e05e76d6",
            "Content-Type": "application/json"
        }
        response = requests.post(url, headers=headers, data=json.dumps(payload))

        # Return status
        return jsonify({
            "status": "success",
            "swarmnode_status": response.status_code,
            "swarmnode_response": response.text
        })
    
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

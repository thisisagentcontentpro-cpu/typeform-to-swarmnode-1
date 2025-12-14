from flask import Flask, request, jsonify
import requests
import urllib3

# Disable SSL warnings (optional)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

app = Flask(__name__)

# ==== Replace these with your actual values ====
SWARMNODE_API_KEY = "1a032cd4a51c4264aa47da33e05e76d6"
AGENT_ID = "f40d1956-56f0-4ed6-b18a-ffdf08e80d55"
# ==============================================

@app.route("/typeform", methods=["POST"])
def handle_typeform():
    data = request.json

    # Transform Typeform payload if needed
    payload = {
        "input": data
    }

    url = f"https://api.swarmnode.com/v1/agents/{AGENT_ID}/input"

    headers = {
        "Authorization": f"Bearer {SWARMNODE_API_KEY}",
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(
            url,
            json=payload,
            headers=headers,
            verify=True  # Ensures SSL is properly verified
        )

        # Return SwarmNode response for debugging
        return jsonify({
            "status": "success",
            "swarmnode_response": response.json()
        }), 200

    except requests.exceptions.SSLError as e:
        return jsonify({
            "status": "error",
            "message": "SSL Error",
            "details": str(e)
        }), 500

    except requests.exceptions.RequestException as e:
        return jsonify({
            "status": "error",
            "message": "Request Failed",
            "details": str(e)
        }), 500


@app.route("/", methods=["GET"])
def index():
    return "Typeform → SwarmNode Webhook is running.", 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)


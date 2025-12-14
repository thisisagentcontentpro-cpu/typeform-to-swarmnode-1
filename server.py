from flask import Flask, request, jsonify
import requests
import logging

app = Flask(__name__)

# Replace these with your actual values
SWARMNODE_API_KEY = "1a032cd4a51c4264aa47da33e05e76d6"
AGENT_ID = "f40d1956-56f0-4ed6-b18a-ffdf08e80d55"

# Enable logging
logging.basicConfig(level=logging.INFO)

@app.route("/typeform", methods=["POST"])
def handle_typeform():
    try:
        # Get incoming Typeform payload
        data = request.json
        logging.info("Received Typeform payload: %s", data)

        # Prepare SwarmNode request
        url = f"https://api.swarmnode.com/v1/agents/{AGENT_ID}/input"
        headers = {
            "Authorization": f"Bearer {SWARMNODE_API_KEY}",
            "Content-Type": "application/json"
        }
        payload = {"input": data}
        logging.info("Sending to SwarmNode: URL=%s, Headers=%s, Payload=%s", url, headers, payload)

        # Send request
        response = requests.post(url, json=payload, headers=headers, timeout=10)
        logging.info("SwarmNode response: %s, Status Code: %s", response.text, response.status_code)

        # Return SwarmNode response
        return jsonify({
            "status": "success",
            "swarmnode_response": response.json()
        }), 200

    except requests.exceptions.RequestException as req_err:
        logging.error("Request error: %s", req_err)
        return jsonify({"status": "error", "message": str(req_err)}), 500

    except Exception as e:
        logging.error("Unhandled exception: %s", e)
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000, debug=True)


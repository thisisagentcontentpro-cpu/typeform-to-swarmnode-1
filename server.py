from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

SWARMNODE_API_KEY = os.environ.get("SWARMNODE_API_KEY")
SWARMNODE_AGENT_ID = os.environ.get("SWARMNODE_AGENT_ID")

@app.route("/", methods=["GET"])
def health_check():
    return "OK", 200

@app.route("/typeform", methods=["POST"])
def handle_typeform():
    try:
        payload = request.json

        if not payload:
            return jsonify({"error": "No JSON payload received"}), 400

        # Extract answers safely
        answers = payload.get("form_response", {}).get("answers", [])

        data = {}
        for answer in answers:
            field_id = answer.get("field", {}).get("id")
            if "text" in answer:
                data[field_id] = answer["text"]
            elif "email" in answer:
                data[field_id] = answer["email"]
            elif "choice" in answer:
                data[field_id] = answer["choice"].get("label")

        swarmnode_payload = {
            "input": data
        }

        headers = {
            "Authorization": f"Bearer {SWARMNODE_API_KEY}",
            "Content-Type": "application/json"
        }

        swarmnode_url = f"https://api.swarmnode.ai/agents/{SWARMNODE_AGENT_ID}/invoke"

        response = requests.post(
            swarmnode_url,
            json=swarmnode_payload,
            headers=headers,
            timeout=30
        )

        return jsonify({
            "status": "sent_to_swarmnode",
            "swarmnode_status": response.status_code,
            "swarmnode_response": response.text
        }), 200

    except Exception as e:
        return jsonify({
            "error": "Server error",
            "details": str(e)
        }), 500


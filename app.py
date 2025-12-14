import os
import ssl
import logging
from flask import Flask, request, jsonify
import requests
from requests.adapters import HTTPAdapter
from urllib3.poolmanager import PoolManager

# -----------------------------
# Logging
# -----------------------------
logging.basicConfig(level=logging.INFO)

# -----------------------------
# Flask app
# -----------------------------
app = Flask(__name__)

# -----------------------------
# Environment variables
# -----------------------------
SWARMNODE_API_KEY = os.getenv("SWARMNODE_API_KEY")
AGENT_ID = os.getenv("AGENT_ID")

if not SWARMNODE_API_KEY or not AGENT_ID:
    logging.error("Missing SWARMNODE_API_KEY or AGENT_ID environment variables")

SWARMNODE_URL = f"https://api.swarmnode.com/v1/agents/{AGENT_ID}/input"

# -----------------------------
# TLS workaround (Render SSL fix)
# -----------------------------
class TLSAdapter(HTTPAdapter):
    def init_poolmanager(self, connections, maxsize, block=False):
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        self.poolmanager = PoolManager(
            num_pools=connections,
            maxsize=maxsize,
            block=block,
            ssl_context=ctx
        )

session = requests.Session()
session.mount("https://", TLSAdapter())

# -----------------------------
# Health check
# -----------------------------
@app.route("/", methods=["GET"])
def health():
    return "OK", 200

# -----------------------------
# Typeform webhook
# -----------------------------
@app.route("/typeform", methods=["POST"])
def typeform_webhook():
    try:
        data = request.get_json(force=True)
        logging.info("Received Typeform payload")

        payload = {
            "input": data
        }

        headers = {
            "Authorization": f"Bearer {SWARMNODE_API_KEY}",
            "Content-Type": "application/json"
        }

        logging.info(f"Sending to SwarmNode agent {AGENT_ID}")

        response = session.post(
            SWARMNODE_URL,
            json=payload,
            headers=headers,
            timeout=30
        )

        logging.info(f"SwarmNode status: {response.status_code}")
        logging.info(response.text)

        return jsonify({
            "status": "sent",
            "swarmnode_status": response.status_code
        }), 200

    except Exception as e:
        logging.exception("Webhook failure")
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

# -----------------------------
# Run app
# -----------------------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)



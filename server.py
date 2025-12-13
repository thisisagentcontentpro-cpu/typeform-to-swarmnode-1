import os
import json
import requests
from flask import Flask, request

app = Flask(__name__)

# Endpoint that Typeform will send webhook data to
@app.route('/webhook', methods=['POST'])
def typeform_webhook():
    data = request.json
    email = data.get('email', '')
    full_name = data.get('full_name', '')
    plan = data.get('plan', '')
    city = data.get('city', '')
    niche = data.get('niche', '')

    # Call Render API (or any other step to send data to SwarmNode)
    url = 'https://your-render-api-url.com'  # Replace with your actual Render API URL
    headers = {'Content-Type': 'application/json'}
    payload = {
        'email': email,
        'full_name': full_name,
        'plan': plan,
        'city': city,
        'niche': niche
    }

    response = requests.post(url, headers=headers, data=json.dumps(payload))
    return "Webhook received and data forwarded", 200


if __name__ == "__main__":
    app.run(debug=True)

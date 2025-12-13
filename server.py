from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/typeform-webhook", methods=["POST"])
def typeform_webhook():
    data = request.json
    # For now, just print it to confirm it works
    print("Received Typeform payload:", data)
    return jsonify({"status": "success"})

if __name__ == "__main__":
    app.run(debug=True)

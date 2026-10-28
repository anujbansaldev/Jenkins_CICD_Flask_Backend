import os

from flask import Flask, request, jsonify

app = Flask(__name__)


@app.route("/api/health", methods=["GET"])
def health():
    return jsonify({
        "status": "success",
        "message": "Flask backend is running" 
    })


@app.route("/api/submit", methods=["POST"])
def submit_form():
    data = request.get_json(silent=True) or {}

    name = data.get("name", "").strip()
    email = data.get("email", "").strip()
    message = data.get("message", "").strip()

    if not name or not email or not message:
        return jsonify({
            "status": "error",
            "message": "All fields are required"
        }), 400

    return jsonify({
        "status": "success",
        "message": "Form submitted successfully",
        "data": {
            "name": name,
            "email": email,
            "message": message
        }
    }), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", "5000")), debug=False)

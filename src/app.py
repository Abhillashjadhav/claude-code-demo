from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/health", methods=["GET"])
def health():
    return jsonify(status="ok"), 200

@app.route("/echo", methods=["POST"])
def echo():
    data = request.json or {}
    return jsonify(received=data), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

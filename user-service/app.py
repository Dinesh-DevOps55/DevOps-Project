"""
Minimal user-service API for cloud-native DevOps demos.
"""

from flask import Flask, jsonify

app = Flask(__name__)


@app.get("/healthz")
def healthz():
    # Liveness/readiness endpoint for Kubernetes probes.
    return jsonify({"status": "ok", "service": "user-service"}), 200


@app.get("/users")
def get_users():
    # Static payload to keep the sample simple and beginner-friendly.
    return jsonify(
        [
            {"id": 1, "name": "Alice"},
            {"id": 2, "name": "Bob"},
            {"id": 3, "name": "Charlie"},
        ]
    )


if __name__ == "__main__":
    # Bind to all interfaces so the container can expose this port.
    app.run(host="0.0.0.0", port=5000)

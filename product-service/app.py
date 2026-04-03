"""
Minimal product-service API for cloud-native DevOps demos.
"""

from flask import Flask, jsonify

app = Flask(__name__)


@app.get("/healthz")
def healthz():
    # Liveness/readiness endpoint for Kubernetes probes.
    return jsonify({"status": "ok", "service": "product-service"}), 200


@app.get("/products")
def get_products():
    # Static payload to keep the sample simple and beginner-friendly.
    return jsonify(
        [
            {"id": 101, "name": "Laptop", "price": 1200},
            {"id": 102, "name": "Keyboard", "price": 80},
            {"id": 103, "name": "Mouse", "price": 40},
        ]
    )


if __name__ == "__main__":
    # Bind to all interfaces so the container can expose this port.
    app.run(host="0.0.0.0", port=5001)

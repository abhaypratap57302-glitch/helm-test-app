import os
import socket

from flask import Flask, jsonify

app = Flask(__name__)

# These can be set from Helm (values.yaml -> env in deployment.yaml)
MESSAGE = os.getenv("APP_MESSAGE", "Hello from my Helm test app!")
VERSION = os.getenv("APP_VERSION", "1.0.0")


@app.route("/")
def home():
    # "pod" shows which pod answered, useful when replicaCount > 1
    return jsonify(message=MESSAGE, version=VERSION, pod=socket.gethostname())


@app.route("/health")
def health():
    return jsonify(status="ok"), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

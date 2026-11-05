import os
import json
from flask import Flask, request, jsonify

app = Flask(__name__)

DATA_DIR = "data"
PLUGINS_DIR = "plugins"
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(PLUGINS_DIR, exist_ok=True)

@app.get("/")
def home():
    return jsonify({
        "status": "ok",
        "message": "Private server is running",
        "endpoints": ["/health", "/plugins", "/config"]
    })

@app.get("/health")
def health():
    return jsonify({"ok": True})

@app.get("/plugins")
def plugins():
    files = []
    for name in os.listdir(PLUGINS_DIR):
        if name.endswith(".py"):
            files.append(name)
    return jsonify({"plugins": files})

@app.post("/config")
def save_config():
    data = request.get_json(force=True)
    with open(os.path.join(DATA_DIR, "config.json"), "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    return jsonify({"saved": True, "data": data})

@app.get("/config")
def get_config():
    path = os.path.join(DATA_DIR, "config.json")
    if not os.path.exists(path):
        return jsonify({})
    with open(path, "r", encoding="utf-8") as f:
        return jsonify(json.load(f))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", "8080")))

from flask import Flask, jsonify
import psutil
import datetime
import platform

app = Flask(__name__)

# ─── Endpoint 1: /health ───────────────────────────────────────
@app.route('/health')
def health():
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.datetime.now().isoformat(),
        "message": "DevOps Health Monitor is running!"
    })

# ─── Endpoint 2: /metrics ──────────────────────────────────────
@app.route('/metrics')
def metrics():
    return jsonify({
        "cpu_percent": psutil.cpu_percent(interval=1),
        "ram_percent": psutil.virtual_memory().percent,
        "ram_total_gb": round(psutil.virtual_memory().total / (1024**3), 2),
        "ram_used_gb": round(psutil.virtual_memory().used / (1024**3), 2),
        "disk_percent": psutil.disk_usage('/').percent,
        "disk_total_gb": round(psutil.disk_usage('/').total / (1024**3), 2),
        "platform": platform.system(),
        "timestamp": datetime.datetime.now().isoformat()
    })

# ─── Endpoint 3: / (Home) ──────────────────────────────────────
@app.route('/')
def home():
    return jsonify({
        "project": "DevOps System Health Monitor",
        "author": "Akshay Kumar",
        "endpoints": ["/health", "/metrics"]
    })

# ─── Run the app ───────────────────────────────────────────────
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
from flask import Flask, jsonify
import psutil
import datetime
import platform

app = Flask(__name__)

@app.route('/health')
def health():
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.datetime.now().isoformat(),
        "message": "DevOps Health Monitor is running!"
    })

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

@app.route('/')
def home():
    return jsonify({
        "project": "DevOps System Health Monitor",
        "author": "Akshay Surabathula",
        "endpoints": ["/health", "/metrics", "/dashboard"]
    })

@app.route('/dashboard')
def dashboard():
    return '''
<!DOCTYPE html>
<html>
<head>
    <title>DevOps Health Monitor</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body { font-family: -apple-system, BlinkMacSystemFont, sans-serif; background: #f5f5f5; color: #1a1a1a; }
        .container { max-width: 800px; margin: 0 auto; padding: 2rem 1rem; }
        .header { display: flex; align-items: center; justify-content: space-between; margin-bottom: 2rem; }
        .header h1 { font-size: 22px; font-weight: 500; }
        .badge { display: flex; align-items: center; gap: 6px; background: #d4f5e2; color: #166534; font-size: 13px; padding: 5px 12px; border-radius: 8px; }
        .dot { width: 8px; height: 8px; border-radius: 50%; background: #16a34a; animation: pulse 2s infinite; }
        @keyframes pulse { 0%,100%{opacity:1} 50%{opacity:0.4} }
        .cards { display: grid; grid-template-columns: repeat(3, 1fr); gap: 12px; margin-bottom: 1.5rem; }
        .card { background: #efefef; border-radius: 8px; padding: 1rem; }
        .card-label { font-size: 11px; color: #666; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 6px; }
        .card-value { font-size: 28px; font-weight: 500; }
        .card-sub { font-size: 12px; color: #888; margin-top: 4px; }
        .bar-row { background: white; border: 1px solid #e5e5e5; border-radius: 12px; padding: 1rem 1.25rem; margin-bottom: 1rem; }
        .bar-header { display: flex; justify-content: space-between; margin-bottom: 10px; }
        .bar-title { font-size: 14px; font-weight: 500; }
        .bar-pct { font-size: 14px; color: #666; }
        .bar-track { height: 8px; background: #f0f0f0; border-radius: 4px; overflow: hidden; }
        .bar-fill { height: 100%; border-radius: 4px; transition: width 0.8s ease; }
        .bar-meta { display: flex; justify-content: space-between; margin-top: 6px; font-size: 12px; color: #999; }
        .footer { margin-top: 1.5rem; display: flex; justify-content: space-between; font-size: 12px; color: #999; }
        .refresh-tag { background: #efefef; padding: 4px 10px; border-radius: 8px; }
        @media (max-width: 500px) { .cards { grid-template-columns: 1fr 1fr; } .cards .card:last-child { grid-column: span 2; } }
    </style>
</head>
<body>
<div class="container">
    <div class="header">
        <h1>DevOps Health Monitor</h1>
        <div class="badge"><div class="dot"></div> <span id="status-text">checking...</span></div>
    </div>

    <div class="cards">
        <div class="card">
            <div class="card-label">CPU Usage</div>
            <div class="card-value" id="cpu-pct">--</div>
            <div class="card-sub">percent used</div>
        </div>
        <div class="card">
            <div class="card-label">RAM Used</div>
            <div class="card-value" id="ram-pct">--</div>
            <div class="card-sub" id="ram-sub">-- GB / -- GB</div>
        </div>
        <div class="card">
            <div class="card-label">Disk Used</div>
            <div class="card-value" id="disk-pct">--</div>
            <div class="card-sub" id="disk-sub">-- GB total</div>
        </div>
    </div>

    <div class="bar-row">
        <div class="bar-header">
            <span class="bar-title">CPU</span>
            <span class="bar-pct" id="cpu-bar-label">--</span>
        </div>
        <div class="bar-track">
            <div class="bar-fill" id="cpu-bar" style="width:0%; background:#378ADD;"></div>
        </div>
        <div class="bar-meta"><span>0%</span><span>100%</span></div>
    </div>

    <div class="bar-row">
        <div class="bar-header">
            <span class="bar-title">RAM</span>
            <span class="bar-pct" id="ram-bar-label">--</span>
        </div>
        <div class="bar-track">
            <div class="bar-fill" id="ram-bar" style="width:0%; background:#1D9E75;"></div>
        </div>
        <div class="bar-meta"><span>0 GB</span><span id="ram-max">-- GB total</span></div>
    </div>

    <div class="bar-row">
        <div class="bar-header">
            <span class="bar-title">Disk</span>
            <span class="bar-pct" id="disk-bar-label">--</span>
        </div>
        <div class="bar-track">
            <div class="bar-fill" id="disk-bar" style="width:0%; background:#BA7517;"></div>
        </div>
        <div class="bar-meta"><span>0 GB</span><span id="disk-max">-- GB total</span></div>
    </div>

    <div class="footer">
        <span id="platform">Platform: --</span>
        <span class="refresh-tag">auto-refresh: 5s</span>
    </div>
</div>

<script>
function fetchData() {
    fetch('/metrics')
        .then(r => r.json())
        .then(d => {
            document.getElementById('cpu-pct').textContent = d.cpu_percent.toFixed(1) + '%';
            document.getElementById('ram-pct').textContent = d.ram_percent.toFixed(1) + '%';
            document.getElementById('disk-pct').textContent = d.disk_percent.toFixed(1) + '%';
            document.getElementById('ram-sub').textContent = d.ram_used_gb + ' GB / ' + d.ram_total_gb + ' GB';
            document.getElementById('disk-sub').textContent = d.disk_total_gb + ' GB total';
            document.getElementById('cpu-bar').style.width = d.cpu_percent + '%';
            document.getElementById('ram-bar').style.width = d.ram_percent + '%';
            document.getElementById('disk-bar').style.width = d.disk_percent + '%';
            document.getElementById('cpu-bar-label').textContent = d.cpu_percent.toFixed(1) + '%';
            document.getElementById('ram-bar-label').textContent = d.ram_used_gb + ' GB / ' + d.ram_total_gb + ' GB';
            document.getElementById('disk-bar-label').textContent = d.disk_percent.toFixed(1) + '%';
            document.getElementById('ram-max').textContent = d.ram_total_gb + ' GB total';
            document.getElementById('disk-max').textContent = d.disk_total_gb + ' GB total';
            document.getElementById('platform').textContent = 'Platform: ' + d.platform + ' (AWS EC2)';
        });

    fetch('/health')
        .then(r => r.json())
        .then(d => {
            document.getElementById('status-text').textContent = d.status;
        });
}

fetchData();
setInterval(fetchData, 5000);
</script>
</body>
</html>
'''

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
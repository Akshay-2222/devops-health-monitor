# DevOps System Health Monitor 🖥️

A live system health monitoring API and dashboard built with Python, Docker, and deployed on AWS EC2 with automated CI/CD using GitHub Actions.


---

## What This Project Does

This project monitors a live AWS EC2 server and exposes real-time system metrics — CPU usage, RAM, and disk space — through a REST API and a visual dashboard that auto-refreshes every 5 seconds.

---

## Live Endpoints

| Endpoint | Description |
|----------|-------------|
| `/` | Project info and available endpoints |
| `/health` | Server health status check |
| `/metrics` | Live CPU, RAM, and disk metrics (JSON) |
| `/dashboard` | Visual live metrics dashboard |

---

## Tech Stack

| Technology | Purpose |
|------------|---------|
| Python + Flask | REST API and dashboard server |
| psutil | Live system metrics collection |
| Docker | Application containerization |
| AWS EC2 | Cloud deployment (Mumbai region) |
| GitHub Actions | Automated CI/CD pipeline |
| HTML + CSS + JavaScript | Live updating dashboard UI |

---

## Project Structure
```
devops-health-monitor/
├── app/
│   ├── app.py              # Flask API with all endpoints
│   ├── requirements.txt    # Python dependencies
│   └── Dockerfile          # Container build instructions
└── .github/
    └── workflows/
        └── deploy.yml      # GitHub Actions CI/CD pipeline
```

---

## How to Run Locally

**1. Clone the repository:**
```bash
git clone https://github.com/YOUR_USERNAME/devops-health-monitor.git
cd devops-health-monitor/app
```

**2. Run with Docker:**
```bash
docker build -t health-monitor .
docker run -p 5000:5000 health-monitor
```

**3. Visit in browser:**
```
http://localhost:5000/dashboard
```

---

## CI/CD Pipeline

Every push to the `main` branch automatically:

1. Sets up Python 3.13 environment
2. Installs all dependencies
3. Tests the `/health` endpoint
4. Builds the Docker image
5. Confirms successful build

---

## What I Learned

- Building REST APIs with Python and Flask
- Containerizing applications with Docker
- Deploying to AWS EC2 using SSH
- Setting up automated CI/CD with GitHub Actions
- Writing live-updating dashboards with JavaScript fetch API

---

## Author

**Akshay Kumar Surabathula**  
Aspiring Cloud Engineer  
[GitHub](https://github.com/Akshay-2222)

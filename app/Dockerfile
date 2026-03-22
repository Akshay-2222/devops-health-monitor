FROM python:3.13-slim

WORKDIR /app

# Add this new line — installs gcc compiler that psutil needs
RUN apt-get update && apt-get install -y gcc python3-dev && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY app.py .

EXPOSE 5000

CMD ["python3", "app.py"]
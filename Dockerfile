# 1. Start with a lightweight, official Python base image
FROM python:3.11-slim

# 2. Set the working directory inside the container system
WORKDIR /app

# 3. Copy only dependency files first to utilize Docker's caching layers
COPY requirements.txt .

# 4. Install production dependencies securely
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copy the structural application directories and scripts into the build
COPY src/ ./src
COPY main.py .
COPY earthquakes_feed.json .

# 6. Establish the execution directive when the container spins up
CMD ["python", "main.py"]

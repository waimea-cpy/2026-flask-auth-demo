# Specific Python version to use
FROM python:3.12-slim

WORKDIR /app

# Install dependencies first - Docker caches this layer so it
# only re-runs when requirements.txt changes (faster rebuilds)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the project in
COPY . .

# Flask needs to listen on all interfaces, not just localhost,
# so requests from outside the container can reach it
ENV FLASK_RUN_HOST=0.0.0.0

CMD ["flask", "run"]


# syntax=docker/dockerfile:1

ARG PYTHON_VERSION=3.13.1
FROM python:${PYTHON_VERSION}-slim AS base

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# System deps if needed (you can add more)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
 && rm -rf /var/lib/apt/lists/*

# Create a non-root user with a real home directory
ARG UID=10001
RUN useradd \
    --create-home \
    --home-dir /home/appuser \
    --shell /bin/bash \
    --uid "${UID}" \
    appuser

# Workdir for the app
WORKDIR /8WayStrategy

# Install Python deps as root (for speed / cache)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app code
COPY . .

# Make sure app files are owned by appuser
RUN chown -R appuser:appuser /8WayStrategy

# Switch to non-root user
USER appuser
ENV HOME=/home/appuser

# Streamlit default port
EXPOSE 8501

# Run Streamlit
CMD ["streamlit", "run", "roulette.py", "--server.port=8501", "--server.address=0.0.0.0"]
# docker build -t roulette-app .
# docker run -p 8501:8501 roulette-app
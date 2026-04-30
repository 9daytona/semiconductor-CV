FROM mcr.microsoft.com/devcontainers.python:3.10

RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0

WORKDIR /workspace

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
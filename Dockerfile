# Use the Python 3.9 image as the base
FROM python:3.12.0-slim-bookworm

COPY requirements.txt .

RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc libc6-dev \
    && rm -rf /var/lib/apt/lists/* \
    && pip install cryptography

RUN pip install -r requirements.txt
# Set the working directory
WORKDIR /app

# Install dependencies specified in requirements.txt

# Copy the application code to the working directory
COPY . .

# Run the Python script
ENTRYPOINT ["python", "main.py"]

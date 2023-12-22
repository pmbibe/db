FROM python:3.12.0-slim-bookworm as builder

ARG buildArg

LABEL builID=$buildArg

LABEL stage="builder"

COPY requirements.txt .

RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc libc6-dev \
    && rm -rf /var/lib/apt/lists/* \
    && pip install cryptography
	
RUN pip install --no-cache-dir --upgrade -r requirements.txt

FROM python:3.12.0-slim-bookworm

WORKDIR /app

COPY --from=builder /root/.local /root/.local

COPY . .

# Run the Python script
ENTRYPOINT ["python", "main.py"]

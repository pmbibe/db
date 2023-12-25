# Use the Python 3.12 image as the base
FROM python:3.12.0-slim-bookworm as builder

ARG buildArg

LABEL builID=$buildArg

LABEL stage="builder"

RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc libc6-dev \
    && rm -rf /var/lib/apt/lists/* \
    && pip install cryptography


COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade -r requirements.txt

FROM python:3.12.0-slim-bookworm



RUN apt-get update \
    && apt-get install -y --no-install-recommends libaio1 \
    && rm -rf /var/lib/apt/lists/*

COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages

WORKDIR /opt/oracle

COPY instantclient_21_12 /opt/oracle/instantclient_21_12

ENV LD_LIBRARY_PATH /opt/oracle/instantclient_21_12:$LD_LIBRARY_PATH

WORKDIR /app

COPY . .


# Run the Python script
ENTRYPOINT ["python", "main.py"]

# Use the Python 3.12 image as the base
FROM python:3.12.0-slim-bookworm as builder

ARG buildArg

LABEL builID=$buildArg

LABEL stage="builder"

COPY requirements.txt .

RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc libc6-dev \
    && rm -rf /var/lib/apt/lists/* \
    && pip install cryptography \ 
    && apt-get install -y libaio1 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /opt/oracle

COPY instantclient_21_12 /opt/oracle/instantclient_21_12
	
RUN pip install --no-cache-dir --upgrade -r requirements.txt

FROM python:3.12.0-slim-bookworm

WORKDIR /app

COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages

ENV LD_LIBRARY_PATH /opt/oracle/instantclient_21_12:$LD_LIBRARY_PATH

COPY . .


# Run the Python script
ENTRYPOINT ["python", "main.py"]

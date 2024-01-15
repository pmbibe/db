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

FROM python:3.12.0-slim-bookworm as middler

ARG buildArg

LABEL builID=$buildArg

LABEL stage="middler"

WORKDIR /app

COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages

ENV LD_LIBRARY_PATH /opt/oracle/instantclient_21_12:$LD_LIBRARY_PATH

COPY . .


# Use an official Python slim image as the base
FROM python:3.12.0-slim-bookworm

# Install necessary dependencies, including wine64 and PyInstaller
RUN apt-get update && \
    apt-get install -y wine64 && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* && \
    pip install pyinstaller
    
# Set up Wine environment variables
ENV WINEARCH=win64 \
    WINEPREFIX=/root/.wine

# Set the working directory
WORKDIR /app

# Optionally, copy your source code into the container
COPY --from=middler /app .

# Run PyInstaller to create a standalone Windows executable
RUN wine pyinstaller --onefile --noconsole db-tool.py

# Set the default command to run the generated executable
CMD ["wine", "dist/db-tool.exe"]

FROM python:3.8-slim

ENV PIP_NO_CACHE_DIR=1 \
    JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64/ \
    PYTHONPATH=/app \
    SIGNAL_CLI_VERSION=0.9.1

# Install OpenJDK-8
RUN apt-get update && \
    mkdir -p /usr/share/man/man1 && \
    apt-get install -y \
        default-jre \
        wget \
        ca-certificates-java \
        dos2unix && \
    rm -rf /var/lib/apt/lists/* && \
    update-ca-certificates -f

# Install signal-cli
WORKDIR /tmp
RUN wget -q https://github.com/AsamK/signal-cli/releases/download/v${SIGNAL_CLI_VERSION}/signal-cli-${SIGNAL_CLI_VERSION}.tar.gz && \
    tar xf /tmp/signal-cli-${SIGNAL_CLI_VERSION}.tar.gz -C /opt && \
    ln -sf /opt/signal-cli-${SIGNAL_CLI_VERSION}/bin/signal-cli /usr/local/bin/

WORKDIR /app
COPY scripts/register-number.sh .
RUN dos2unix ./register-number.sh
COPY . .
RUN pip install -r requirements.txt && pip install -e .

CMD ["signal-scanner-bot"]

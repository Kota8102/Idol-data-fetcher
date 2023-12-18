FROM node:18

# Install basic development tools
RUN apt update && apt install -y less man-db sudo

# Ensure default `node` user has access to `sudo`
ARG USERNAME=node
RUN echo $USERNAME ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/$USERNAME \
    && chmod 0440 /etc/sudoers.d/$USERNAME

# Set `DEVCONTAINER` environment variable to help with orientation
ENV DEVCONTAINER=true

# Install Python, pip, and setup a virtual environment
RUN apt-get update && \
    apt-get install -y python3 python3-pip python3-venv && \
    python3 -m venv /opt/venv && \
    rm -rf /var/lib/apt/lists/*

# Change ownership of the virtual environment to `node` user
RUN chown -R $USERNAME:$USERNAME /opt/venv

# Activate virtual environment automatically on each shell session
ENV PATH="/opt/venv/bin:$PATH"

# Switch to `node` user
USER $USERNAME

# Set default work directory
WORKDIR /app

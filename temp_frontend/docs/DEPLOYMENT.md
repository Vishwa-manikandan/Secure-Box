# Deployment Guide

## Production Requirements
- Docker Engine 24.0+
- Docker Compose v2.0+
- Minimum 4GB RAM, 2 CPUs

## Deployment Steps
1. **Environment Configuration**:
   Ensure `.env` contains valid `OPENAI_API_KEY` and `GITHUB_TOKEN`.

2. **Infrastructure Setup**:
   We recommend deploying the Sandbox Broker on a dedicated host separate from the main API to ensure total isolation.

3. **Launch**:
   ```bash
   docker-compose up -d
   ```

## Sandbox Security Configuration
To enhance isolation, we recommend:
- Using **Rootless Docker** on the sandbox host.
- Implementing a **Docker Socket Proxy** to restrict API access to only `container create` and `container stop`.
- Configuring **AppArmor** or **SELinux** profiles for the skill containers.

# backend/create_vm.py
import os
import requests
from dotenv import load_dotenv

load_dotenv()

VULTR_API_KEY = os.getenv("VULTR_API_KEY")
DOCKER_IMAGE = os.getenv("DOCKER_IMAGE")


if not VULTR_API_KEY:
    raise ValueError("VULTR_API_KEY is not set.")

headers = {
    "Authorization": f"Bearer {VULTR_API_KEY}",
    "Content-Type": "application/json"
}

def create_vm(bot_name: str):
    label = bot_name.replace(" ", "-").lower()[:20]
    hostname = label
    region = "ewr"  # Choose working region like 'ams', 'ewr', 'ord'
    plan = "vc2-1c-2gb"
    os_id = 1743  # Ubuntu 22.04 x64

    # This assumes the Docker image is public on Docker Hub
    user_data = f"""#!/bin/bash
apt update && apt install -y docker.io
docker run -d -p 8000:8000 --env BOT_NAME="{bot_name}" {DOCKER_IMAGE}
"""

    payload = {
        "region": region,
        "plan": plan,
        "os_id": os_id,
        "label": label,
        "hostname": hostname,
        "user_data": user_data
    }

    response = requests.post("https://api.vultr.com/v2/instances", headers=headers, json=payload)

    if response.status_code == 202:
        return response.json()["instance"]
    else:
        raise Exception(f"Deployment failed: {response.text}")

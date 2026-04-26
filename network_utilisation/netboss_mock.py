import requests
import time
import random
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from env import settings
from datetime import datetime, timezone
from log_config import get_logger

logger = get_logger(__name__)

# The URL of the middleware server
MIDDLEWARE_API_URL = settings.MIDDLEWARE_API_URL_NETBOSS


# The circuit we seeded in the database (Provisioned for 100 Mbps)
TARGET_CID = "CID-BARN-10023"

def generate_telemetry(is_spiking: bool = False):
    """Generates a realistic utilization payload."""
    # If spiking, push utilization between 98 and 100 Mbps.
    # If normal, keep it safely between 40 and 70 Mbps.
    if is_spiking:
        utilization = round(random.uniform(99.0, 501.0), 2)
    else:
        utilization = round(random.uniform(40.0, 70.0), 2)

    return {
        "circuit_id": TARGET_CID,
        "utilization_mbps": utilization,
        "timestamp": datetime.now(timezone.utc).isoformat()
    }

def run_simulation():
    logger.info(f"Starting Netboss Simulator targeting {TARGET_CID}...")
    logger.info(f"Sending data to {MIDDLEWARE_API_URL}\n")
    
    tick_count = 0
    
    while True:
        tick_count += 1
        
        # forcing Maxout every 5 ticks to trigger netboss Notification
        is_spiking = (tick_count % 5 == 0) # returns a bool
        
        payload = generate_telemetry(is_spiking)
        
        try:
            response = requests.post(MIDDLEWARE_API_URL, json=payload)
            
            if response.status_code == 201:
                logger.info(f"[SUCCESS] Sent {payload['utilization_mbps']} Mbps | API Response: 201 | {response.json()}")
            else:
                logger.error(f"[ERROR] API returned {response.status_code}: {response.text}")
                
        except requests.exceptions.ConnectionError:
            logger.error("[FATAL] Could not connect to the API. Is Middleware running?")
            break

        # Wait 3 seconds before sending the next telemetry ping
        time.sleep(3)

if __name__ == "__main__":
    run_simulation()
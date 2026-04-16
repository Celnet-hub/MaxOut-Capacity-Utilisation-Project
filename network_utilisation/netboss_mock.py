import requests
import time
import random
from env import settings
from datetime import datetime, timezone

# The URL of the middleware server
MIDDLEWARE_API_URL = settings.MIDDLEWARE_API_URL_NETBOSS


# The circuit we seeded in the database (Provisioned for 100 Mbps)
TARGET_CID = "CID-BARN-10023"

def generate_telemetry(is_spiking: bool = False):
    """Generates a realistic utilization payload."""
    # If spiking, push utilization between 98 and 100 Mbps.
    # If normal, keep it safely between 40 and 70 Mbps.
    if is_spiking:
        utilization = round(random.uniform(98.0, 100.0), 2)
    else:
        utilization = round(random.uniform(40.0, 70.0), 2)

    return {
        "circuit_id": TARGET_CID,
        "utilization_mbps": utilization,
        "timestamp": datetime.now(timezone.utc).isoformat()
    }

def run_simulation():
    print(f"Starting Netboss Simulator targeting {TARGET_CID}...")
    print(f"Sending data to {MIDDLEWARE_API_URL}\n")
    
    tick_count = 0
    
    while True:
        tick_count += 1
        
        # forcing Maxout every 5 ticks to trigger netboss Notification
        is_spiking = (tick_count % 5 == 0) # returns a bool
        
        payload = generate_telemetry(is_spiking)
        
        try:
            response = requests.post(MIDDLEWARE_API_URL, json=payload)
            
            if response.status_code == 201:
                print(f"[SUCCESS] Sent {payload['utilization_mbps']} Mbps | API Response: 201")
            else:
                print(f"[ERROR] API returned {response.status_code}: {response.text}")
                
        except requests.exceptions.ConnectionError:
            print("[FATAL] Could not connect to the API. Is Middleware running?")
            break

        # Wait 3 seconds before sending the next telemetry ping
        time.sleep(3)

if __name__ == "__main__":
    run_simulation()
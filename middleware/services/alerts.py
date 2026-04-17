from middleware.config.db import SessionLocal # Import the session factory directly
from middleware.models.database import MaxOutEvent, CustomerProduct
from middleware.config.env import settings
import time

circuit_state_cache = {}

def send_email(customer_cid: str, bandwidth: float):
    pass

def async_processing(circuit_id: str, current_utilization: float):
    """
    This function runs entirely in the background, decoupled from the API response.
    """

    print('Asynch processing begins')
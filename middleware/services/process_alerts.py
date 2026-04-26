from middleware.config.db import SessionLocal # Import the session factory directly
from middleware.models.database import MaxOutEvent, CustomerProduct
from middleware.config.env import settings
import time
from log_config import get_logger

logger = get_logger(__name__)

circuit_state_cache = {}

def send_email(customer_cid: str, bandwidth: float):
    return True

def async_processing(circuit_id: str, current_utilization: float):
    """
    This function runs entirely in the background, decoupled from the API response.
    """
    db = SessionLocal()

    logger.info('Begining Asynch processing...................')
    try:
        # get customer product
        product = db.query(CustomerProduct).filter(CustomerProduct.cid == circuit_id).first()
        logger.info(f'Product Details: {product}')
        if not product:
            logger.error(f"[BACKGROUND ERROR] CID {circuit_id} not found")
            return

        # Verify the threshold
        threshold = product.provisioned_bandwidth_mbps * settings.ALERT_THRESHOLD_PCT

        if current_utilization >= threshold:
            logger.info(f"[ALERT RECEIVED] Confirmed Max-Out for {circuit_id}! Processing immediately.")

            # Save event to db.
            new_event = MaxOutEvent(product_id=product.id, notification_sent=False)
            logger.info(f'New Event: {new_event}')
            db.add(new_event)
            db.commit()
            logger.info("[DB WRITE] Event saved to PostgreSQL.")

            # Send Email Notification
            stat = send_email(customer_cid=circuit_id, bandwidth=product.provisioned_bandwidth_mbps)
            if stat:
                new_event.notification_sent = True
                db.commit()
                logger.info("[DB WRITE] Event updated with notification sent to PostgreSQL.")
        else:
            logger.info(f"[NORMAL OPERATION] {circuit_id} is operating within normal parameters ({current_utilization} Mbps).")

    except Exception as e:
        logger.error(f"[SYSTEM ERROR] Failed to process alert: {e}")
        db.rollback()

    finally:
        # Always close the DB session when the background task finishes!
        db.close()
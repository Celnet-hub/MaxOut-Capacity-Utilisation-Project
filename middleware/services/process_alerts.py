from middleware.config.db import SessionLocal # Import the session factory directly
from middleware.models.database import MaxOutEvent, CustomerProduct
from middleware.config.env import settings
import time
from middleware.services.emailing import send_capacity_alert_email
from log_config import get_logger

logger = get_logger(__name__)




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

        # Extract customer details
        account = product.account
        account_name = account.account_name
        
        # Use the first contact available
        contact = account.contacts[0] if account.contacts else None
        if not contact:
            logger.error(f"[BACKGROUND ERROR] No contacts found for account {account_name}")
            return
            
        recipient_email = contact.email_address
        customer_name = f"{contact.first_name} {contact.last_name}"

        # Account Manager details
        am = account.account_manager
        am_name = f"{am.first_name} {am.last_name}" if am else "Unknown"
        am_email = am.email if am else ""

        # CX Manager details
        cx = account.cx_manager
        cx_name = f"{cx.first_name} {cx.last_name}" if cx else "Unknown"
        cx_email = cx.email if cx else ""

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
            stat = send_capacity_alert_email(
                recipient_email=recipient_email,
                customer_name=customer_name,
                circuit_id=circuit_id,
                provisioned_bandwidth=product.provisioned_bandwidth_mbps,
                account_name=account_name,
                am_name=am_name,
                am_email=am_email,
                cx_name=cx_name,
                cx_email=cx_email
            )
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
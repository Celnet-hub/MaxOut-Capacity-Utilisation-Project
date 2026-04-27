# middleware/services/emailing.py
import smtplib
import textwrap
from email.message import EmailMessage
from middleware.config.env import settings
from log_config import get_logger

logger = get_logger(__name__)

def send_capacity_alert_email(
    recipient_email: str, 
    customer_name: str, 
    circuit_id: str, 
    provisioned_bandwidth: float,
    account_name: str,
    am_name: str,
    am_email: str,
    cx_name: str,
    cx_email: str
):
    """
    Constructs and sends an SMTP email alert.
    """
    msg = EmailMessage()
    msg['Subject'] = f"URGENT: Action Required - Network Capacity Alert for {circuit_id}"
    msg['From'] = settings.SMTP_USERNAME
    msg['To'] = recipient_email
    
    cc_emails = [email for email in [am_email, cx_email] if email]
    if cc_emails:
        msg['Cc'] = ", ".join(cc_emails)

    # The Plain Text Email Body (Fallback)
    text_body = textwrap.dedent(f"""\
    Dear {customer_name},

    This is an automated notification from the Network Operations Center regarding your account ({account_name}).

    Please be advised that your circuit ({circuit_id}) is currently operating at 100% of its provisioned capacity ({provisioned_bandwidth} Mbps).

    Sustained utilization at this maximum threshold may lead to degraded network performance and potential service disruption. We strongly recommend initiating an internal review of your network traffic to identify the source of this increased utilization.

    Should you determine that this reflects a sustained increase in your operational requirements, please reach out to your Account Manager, {am_name} ({am_email}), or your Customer Experience Manager, {cx_name} ({cx_email}). They will be happy to assist you in exploring temporary burst capacity or a permanent tier upgrade to ensure optimal service delivery.

    Thank you for your prompt attention to this matter.

    Sincerely,
    Network Operations Center
    """)
    
    # The HTML Email Body (Primary)
    html_body = textwrap.dedent(f"""\
    <html>
      <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333; max-width: 600px; margin: 0 auto;">
        <p>Dear <strong>{customer_name}</strong>,</p>

        <p>This is an automated notification from the Network Operations Center regarding your account (<strong>{account_name}</strong>).</p>

        <p>Please be advised that your circuit (<strong>{circuit_id}</strong>) is currently operating at <span style="color: #d9534f; font-weight: bold;">100%</span> of its provisioned capacity (<strong>{provisioned_bandwidth} Mbps</strong>).</p>

        <p>Sustained utilization at this maximum threshold may lead to degraded network performance and potential service disruption. We strongly recommend initiating an internal review of your network traffic to identify the source of this increased utilization.</p>

        <p>Should you determine that this reflects a sustained increase in your operational requirements, please reach out to your Account Manager, <strong>{am_name}</strong> (<a href="mailto:{am_email}">{am_email}</a>), or your Customer Experience Manager, <strong>{cx_name}</strong> (<a href="mailto:{cx_email}">{cx_email}</a>). They will be happy to assist you in exploring temporary burst capacity or a permanent tier upgrade to ensure optimal service delivery.</p>

        <p>Thank you for your prompt attention to this matter.</p>

        <p>Sincerely,<br>
        <strong>Network Operations Center</strong></p>
      </body>
    </html>
    """)

    msg.set_content(text_body)
    msg.add_alternative(html_body, subtype='html')

    try:
        logger.info(f"Connecting to {settings.SMTP_SERVER}...")
        with smtplib.SMTP(settings.SMTP_SERVER, settings.SMTP_PORT) as server:
            server.starttls()
            server.login(settings.SMTP_USERNAME, settings.SMTP_PASSWORD)
            server.send_message(msg)

        logger.info(f"Alert successfully sent to {recipient_email}")
        return True
    
    except Exception as e:
        logger.error(f"Failed to send email: {e}")
        return False
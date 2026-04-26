import random
from datetime import date, timedelta
from middleware.config.db import SessionLocal 
from middleware.models.database import Employee, CustomerAccount, Contact, CustomerProduct
from log_config import get_logger

logger = get_logger(__name__)

# The restricted email list per your instructions
ALLOWED_EMAILS = ["dubemnwabuisi@gmail.com", "dubemcn@outlook.com"]


def generate_cid(pop_name: str, index: int) -> str:
    # Takes the first 3 letters of the POP, uppercases them, and adds a number
    # "Barnet" -> "BARN" -> "CID-BARN-10001"
    prefix = pop_name[:4].upper()
    return f"CID-{prefix}-{10000 + index}"

def seed_database():
    db = SessionLocal()
    
    try:
        # Fail-safe: Check if we already have data
        if db.query(Employee).first():
            logger.info("Database is already seeded. Drop tables if you want a fresh start.")
            return

        logger.info("Seeding database with mock data...")

        # Create Employees (Account Managers & CX Managers)
        am_1 = Employee(
            first_name="Alice", last_name="Smith", phone_number="+44 20 7946 0958",
            email=random.choice(ALLOWED_EMAILS), department="Sales", status="Active",
            employment_date=date(2021, 5, 10)
        )
        cx_1 = Employee(
            first_name="Bob", last_name="Jones", phone_number="+44 20 7946 0811",
            email=random.choice(ALLOWED_EMAILS), department="Customer Experience", status="Active",
            employment_date=date(2022, 8, 15)
        )
        
        db.add_all([am_1, cx_1])
        db.commit() # Commit so we get their IDs for the next step

        # Create Customer Accounts
        acme_corp = CustomerAccount(
            account_name="Acme Corp UK", account_status="Active",
            account_manager_id=am_1.id, cx_manager_id=cx_1.id
        )
        globex = CustomerAccount(
            account_name="Globex Telecommunications", account_status="Active",
            account_manager_id=am_1.id, cx_manager_id=cx_1.id
        )
        
        db.add_all([acme_corp, globex])
        db.commit() # Commit so we get their IDs for the next step

        # Create Contacts for those accounts
        contact_1 = Contact(
            account_id=acme_corp.id, first_name="Charlie", last_name="Brown",
            email_address=random.choice(ALLOWED_EMAILS), phone_number="+44 7700 900077",
            position="IT Director", status="Active"
        )
        contact_2 = Contact(
            account_id=globex.id, first_name="Diana", last_name="Prince",
            email_address=random.choice(ALLOWED_EMAILS), phone_number="+44 7700 900111",
            position="Network Admin", status="Active"
        )
        
        db.add_all([contact_1, contact_2])

        # 5. Create Customer Products (The crucial part for your API)
        pops = ["Barnet", "Harrow", "Hendon"]
        
        # Product 1: The Barnet product matching your Netboss payload example!
        prod_1 = CustomerProduct(
            account_id=acme_corp.id,
            cid=generate_cid("Barnet", 23), # Generates "CID-BAR-10023"
            provisioned_bandwidth_mbps=100.0,
            burst_capacity_mbps=150.0, 
            pop="Barnet",
            date_provisioned=date(2024, 1, 15)
        )
        
        # Product 2: A Harrow product for variety
        prod_2 = CustomerProduct(
            account_id=globex.id,
            cid=generate_cid("Harrow", 88), # Generates "CID-LON-10088"
            provisioned_bandwidth_mbps=500.0,
            burst_capacity_mbps=0.0, # No burst allowed
            pop="Harrow",
            date_provisioned=date(2025, 6, 1)
        )

        db.add_all([prod_1, prod_2])
        db.commit()

        logger.info("Database seeded successfully!")
        logger.info(f"Use this CID for your API testing: {prod_1.cid} (Provisioned: {prod_1.provisioned_bandwidth_mbps} Mbps)")

    except Exception as e:
        db.rollback()
        logger.error(f"Error seeding database: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    seed_database()
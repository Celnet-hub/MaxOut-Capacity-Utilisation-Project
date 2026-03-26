"""_summary_
This scripts connects to the database and creates the neccessary tables.

- CRITICAL: You must import your models here, even if you don't use them directly in this script. This registers them with the 'Base' metadata so SQLAlchemy knows what tables to create.
"""

from middleware.config.db import db_engine, Base
from middleware.models import database 

def create_database_tables():
    print("Attempting to connect to PostgreSQL...")
    try:
        # This single line connects to the DB and creates all tables defined in your models
        Base.metadata.create_all(bind=db_engine)
        print("Success! All tables have been created in the database.")
    except Exception as e:
        print("Failed to connect or create tables. See error below:")
        print(e)

if __name__ == "__main__":
    create_database_tables()
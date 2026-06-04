import os
import sys

# 1. Set environment variables BEFORE importing config or application
os.environ["PROJECT_NAME"] = "Test MaxOut Capacity Utilisation Project"
os.environ["DATABASE_URL"] = "sqlite:///:memory:"
os.environ["ALERT_THRESHOLD_PCT"] = "1.0"
os.environ["DEBOUNCE_COUNT"] = "3"
os.environ["SMTP_SERVER"] = "smtp.test.com"
os.environ["SMTP_PORT"] = "587"
os.environ["SMTP_USERNAME"] = "test@test.com"
os.environ["SMTP_PASSWORD"] = "password"

# 2. Add project root to sys.path to ensure imports work correctly
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest
from fastapi.testclient import TestClient


@pytest.fixture
def client():
    # Delay import of app until env vars are set
    from middleware.main import app

    with TestClient(app) as c:
        yield c

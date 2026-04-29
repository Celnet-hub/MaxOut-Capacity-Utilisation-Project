# MaxOut Capacity Alerting System

## Problem Statement

The Network Operations team frequently receives calls from customers experiencing service degradation. Upon troubleshooting, it is often observed that these customers are maxing out their provisioned network capacity. 

## Solution & Business Value

This project provides an automated solution to monitor network telemetry, identify "maxout" events, and proactively alert both the customers and internal teams. By ensuring that these maxout events are accurately detected and stored, the Customer Experience (CX) and Account Management (AM) teams can leverage this data to engage customers proactively. This presents a strategic opportunity to offer potential upgrades or burst capacity options, thereby improving customer satisfaction and driving potential revenue growth.

## Features

- **Telemetry Ingestion**: An API (FastAPI) to receive real-time network telemetry data.
- **Automated Threshold Monitoring**: Background processing of telemetry data to identify circuits exceeding 100% capacity.
- **Proactive Notifications**: Automated, beautifully formatted HTML email alerts dispatched to customers, with CX and AM teams CC'd.
- **Event Logging & Storage**: Persistent storage of maxout events in a database to enable future analytics and sales engagements.
- **Network Simulator**: A mock simulator (`netboss_mock.py`) to generate testing data.

## Folder Structure

```
MACOUT_CAPACITY/
├── middleware/
│   ├── __init__.py
│   ├── main.py               # The FastAPI application instance & entry point
│   ├── config/
│   │   ├── __init__.py
│   │   ├── config.py         # Environment variables (e.g., DB connection string)
│   │   └── database.py       # SQLAlchemy Engine and SessionLocal setup
│   ├── models/
│   │   ├── __init__.py
│   │   └── network.py        # SQLAlchemy classes (Customer, Telemetry, etc.)
│   ├── schemas/
│   │   ├── __init__.py
│   │   └── network.py        # Pydantic models (for validating incoming API JSON)
│   ├── api/
│   │   ├── __init__.py
│   │   └── routes.py         # The actual API endpoints (e.g., POST /telemetry)
│   └── services/
│       ├── __init__.py
│       ├── process_alerts.py # Business logic (async processing, threshold checks)
│       └── emailing.py       # Email formatting and delivery system
├── network_utilisation/
│   ├── env.py                # Environment configuration for the simulator
│   └── netboss_mock.py       # The standalone Python script generating mock data
├── log_config.py             # Centralized logging configuration
├── init_db.py                # Database initialization script
├── seed_db.py                # Database seeding script
├── .gitignore
├── Makefile
└── requirements.txt
```

## Development Workflow History

- Set up Database
- Set up models and configs
- Set up schemas for our APIs
- Set up middleware `main.py` entry point
- Set up routes
- Test routes
- Set up netboss simulator
- Test that routes are working just fine
- Set up event-based routing
- Refactor telemetry ingestion to use background processing
- Set up centralized logging across the application
- Upgrade email system to support structured HTML templates

## Makefile Usage

Use the project Makefile from the repository root:

```bash
make help
```

Common commands:

```bash
make install
make editable
make init-db
make seed-db
make run-api
make dev
```

Notes:

- `make install` installs dependencies from `requirements.txt` into `.venv`.
- `make editable` runs `pip install -e .` so package imports work from any directory.
- `make dev` starts `uvicorn` with `--reload` for development.

## Future Tasks

- Migrate data from PostgreSQL to MSSQL
- Use Event-Driven Orchestration to run background processing of alerts
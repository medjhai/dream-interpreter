import os
import logging
from app import app
from models import init_db

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Initialize database
logger.info("Initializing database...")
init_db()
logger.info("Database initialized successfully")

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5002)

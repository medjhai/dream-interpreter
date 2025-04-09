import os
import logging
from app import app

# Configure logging
logging.basicConfig(level=logging.DEBUG)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)

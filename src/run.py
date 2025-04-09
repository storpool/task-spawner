import os
import logging
from app import create_app
from config import get_config
import teamwork

# Load configuration
config = get_config()

# Validate that the task list exists in Teamwork
try:
    teamwork.validate_task_list_exists(config)
except Exception as e:
    logging.error(f"Teamwork task list validation failed: {e}")
    raise SystemExit(1)

# Create Flask app
app = create_app(config)

if __name__ == "__main__":
    if os.getenv("FLASK_ENV") == "development":
        logging.basicConfig(level=logging.DEBUG)
        app.run(host="0.0.0.0", port=5000, debug=True)
    else:
        # Use Gunicorn's logging setup
        gunicorn_logger = logging.getLogger("gunicorn.error")
        app.logger.handlers = gunicorn_logger.handlers
        app.logger.setLevel(gunicorn_logger.level)

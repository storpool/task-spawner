import logging
import sys

from config import get_config
from app import create_app
from teamwork import validate_task_list_exists

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

if __name__ == "__main__":
    config = get_config()
    try:
        validate_task_list_exists(config)
    except ValueError as e:
        logging.critical(f"Teamwork task list validation failed: {e}")
        sys.exit(1)

    app = create_app(config)
    app.run(host="0.0.0.0", port=5000)

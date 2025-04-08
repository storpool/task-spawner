import logging
from config import get_config
from app import create_app
from teamwork import validate_task_list_exists

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

if __name__ == "__main__":
    config = get_config()
    validate_task_list_exists(config)
    app = create_app(config)
    app.run(host="0.0.0.0", port=5000)

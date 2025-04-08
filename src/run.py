import logging
from config import get_config
from app import create_app

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

if __name__ == "__main__":
    config = get_config()
    app = create_app(config)
    app.run(host="0.0.0.0", port=5000)

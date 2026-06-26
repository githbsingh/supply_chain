import logging
import os

os.makedirs(
    "logs",
    exist_ok=True
)
LOG_FILE = "logs/app.log"
# Delete old log file
if os.path.exists(LOG_FILE):
    os.remove(LOG_FILE)

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

logger = logging.getLogger(
    "SupplyChainAI"
)
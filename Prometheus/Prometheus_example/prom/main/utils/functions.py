import os
import random
import time

from prometheus_client import generate_latest
from starlette.responses import Response

from prom.main.custom_metrics.basicMetrics import DB_OPERATION_DURATION
from prom.main.schemas.inventory import Inventory
from prom.main.schemas.item import Item
from dotenv import load_dotenv


# Function to load inventory from .env
def load_inventory_from_env():
    items = os.getenv("INVENTORY_ITEMS")
    if items:
        return [Item.parse_raw(item) for item in items.split(";")]


# Function to save inventory to .env
def save_inventory_to_env(inventory):
    # Serialize the inventory items
    serialized_items = ";".join([item.json() for item in inventory.items])

    # Load the existing .env file
    env_path = os.path.join(os.path.dirname(__file__), '../../../.env')
    load_dotenv(dotenv_path=env_path)

    # Update the environment variable
    os.environ["INVENTORY_ITEMS"] = serialized_items

    # Write the new value to the .env file
    with open(env_path, 'w') as f:
        for key, value in os.environ.items():
            if key == "INVENTORY_ITEMS":
                f.write(f"{key}={serialized_items}\n")


def metrics1():
    return Response(content=generate_latest(), media_type='text/plain')


def calculate_low_stock_percentage(inventory: Inventory):
    low_stock_threshold = 10
    low_stock_count = sum(1 for item in inventory.items if item.amount < low_stock_threshold)
    total_items = len(inventory.items)
    if total_items == 0:
        return 0
    return (low_stock_count / total_items) * 100


def measure_db_operation(func):
    def wrapper(*args, **kwargs):
        with DB_OPERATION_DURATION.time():  # Measure the time taken by the decorated function
            return func(*args, **kwargs)
    return wrapper


@measure_db_operation
def execute_query():
    # Simulate a database query execution
    time.sleep(random.uniform(0.1, 1.0))  # Simulating varying query times

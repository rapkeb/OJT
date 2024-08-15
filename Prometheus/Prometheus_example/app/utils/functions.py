import os
from prometheus_client import generate_latest
from starlette.responses import Response
from app.schemas.inventory import Inventory
from app.schemas.item import Item
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
    env_path = os.path.join(os.path.dirname(__file__), '../../.env')
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

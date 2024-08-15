from dotenv import load_dotenv
from app.utils.functions import load_inventory_from_env
from app.schemas.inventory import Inventory


# Load environment variables from .env file
load_dotenv()

# Create a global instance of Inventory
inventory = Inventory()
inventory.items = load_inventory_from_env()


# Dependency function to provide the inventory instance
def get_inventory() -> Inventory:
    return inventory

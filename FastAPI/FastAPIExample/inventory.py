from fastapi import FastAPI, HTTPException, Body
from pydantic import BaseModel
from typing import List, Annotated
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Model for item information
class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = 12.5
    amount: int  # Quantity of the item

# Model for inventory
class Inventory(BaseModel):
    name: str | None = "Shufersal"
    items: List[Item] = []

# Create a global instance of Inventory
inventory = Inventory()

# Function to load inventory from .env
def load_inventory_from_env():
    items = os.getenv("INVENTORY_ITEMS")
    if items:
        inventory.items = [Item.parse_raw(item) for item in items.split(";")]

# Function to save inventory to .env
def save_inventory_to_env():
    serialized_items = ";".join([item.json() for item in inventory.items])
    if "INVENTORY_ITEMS" in os.environ:
        del os.environ["INVENTORY_ITEMS"]
    with open('.env', 'w') as f:
        f.write('')
    os.environ["INVENTORY_ITEMS"] = serialized_items
    with open('.env', 'a') as f:
        f.write(f"\nINVENTORY_ITEMS={serialized_items}")

# Load the inventory at startup
load_inventory_from_env()


app = FastAPI()

@app.post("/add_item/")
async def add_item(item: Item):
    for existing_item in inventory.items:
        if existing_item.name == item.name:
            existing_item.amount += item.amount
            save_inventory_to_env()
            return {"message": f"Item '{item.name}' quantity updated to {existing_item.amount}"}
    
    inventory.items.append(item)
    save_inventory_to_env()
    return {"message": "Item added successfully", "item": item}

@app.post("/buy_item/")
async def buy_item(name: Annotated[str, Body()], amount: Annotated[int, Body()]):
    for item in inventory.items:
        if item.name == name:
            if item.amount < amount:
                raise HTTPException(status_code=400, detail="Not enough items in stock")
            item.amount -= amount
            if item.amount == 0:
                inventory.items.remove(item)
            save_inventory_to_env()
            return {"message": f"{amount} units of '{item.name}' purchased successfully", "remaining": item.amount}
    raise HTTPException(status_code=404, detail="Item not found")

@app.get("/items/")
async def get_items():
    return inventory.items

from fastapi import APIRouter, Body, Depends
from app.crud.item import root1, add_item1, buy_item1
from app.schemas.inventory import Inventory
from app.schemas.item import Item
from typing import Annotated
from app.utils.inventory_helper import get_inventory  # Importing get_inventory from app.py



# Create an instance of APIRouter
router = APIRouter()


@router.get("/")
async def root(inventory: Inventory = Depends(get_inventory)):
    items = await root1(inventory)
    return items


@router.post("/add_item/")
async def add_item(item: Item, inventory: Inventory = Depends(get_inventory)):
    message = await add_item1(item, inventory)
    return message


@router.post("/buy_item/")
async def buy_item(name: Annotated[str, Body()], amount: Annotated[int, Body()], inventory: Inventory = Depends(get_inventory)):
    message = await buy_item1(name, amount, inventory)
    return message



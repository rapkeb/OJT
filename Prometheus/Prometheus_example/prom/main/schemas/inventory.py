from pydantic import BaseModel
from typing import List
from .item import Item


# Model for inventory
class Inventory(BaseModel):
    name: str | None = "Shufersal"
    items: List[Item] = []

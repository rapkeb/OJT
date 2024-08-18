from pydantic import BaseModel


# Model for item information
class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = 12.5
    amount: int  # Quantity of the item

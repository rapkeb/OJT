from fastapi import FastAPI, status, Body
from typing import Annotated, Optional
from pydantic import BaseModel, EmailStr, HttpUrl

app = FastAPI()

# Model for base user information
class BaseUser(BaseModel):
    username: str  # Username of the user
    email: EmailStr  # Email address of the user
    full_name: str | None = None  # Optional full name of the user

# Model for user input including password
class UserIn(BaseUser):
    password: str  # Password for the user

# Endpoint to create a new user
@app.post("/user/")
async def create_user(user: UserIn) -> BaseUser:
    """
    Create a new user with the provided details.

    Args:
        user (UserIn): User details including username, email, full name, and password.

    Returns:
        BaseUser: The created user details.
    """
    return user

# Model for video information
class Video(BaseModel):
    url: HttpUrl  # URL of the video
    name: str | None = None  # Optional name of the video

# Model for event information
class Event(BaseModel):
    name: str  # Name of the event
    description: str | None = None  # Optional description of the event
    tags: list[str] = []  # List of tags associated with the event
    videos: Optional[list[Video]]  # Optional list of videos related to the event

    # Extra configuration for JSON schema examples
    model_config = {
        "json_schema_extra" : {
            "examples": [
                {
                "name": "Annual Tech Conference",
                "description": "A conference showcasing the latest in technology and innovation.",
                "tags": ["technology", "conference", "innovation"],  # Tags as a list of strings
                "videos": [
                    {
                        "url": "https://www.example.com/video1",  # URL of the first video
                        "name": "Keynote Presentation"  # Name of the first video
                    },
                    {
                        "url": "https://www.example.com/video2",  # URL of the second video
                        "name": "Tech Panel Discussion"  # Name of the second video
                    }
                ]
            }
            ]
        }
    }

# Endpoint to update an existing event
@app.put("/events/{event_id}", status_code=status.HTTP_200_OK)
async def update_event(event_id: int, event: Event):
    """
    Update an existing event with new details.

    Args:
        event_id (int): The ID of the event to be updated.
        event (Event): New details for the event.

    Returns:
        dict: A summary of the updated event including its ID, name, tags, and video information.
    """
    # Extract event details
    event_name = event.name
    event_tags = event.tags

    # Prepare response with event summary
    results = {
        "event_id": event_id,
        "event_name": event_name,
        "event_tags": event_tags,
        "videos": "There are videos for the event" if event.videos else "No videos"
    }
    return results

# Model for item information
class Item(BaseModel):
    name: str  # Name of the item
    description: str | None = None  # Optional description of the item
    price: float  # Price of the item
    tax: float | None = 12.5  # Optional tax rate (default is 12.5)

# Endpoint to update an existing item
@app.put("/items/{item_id}")
async def update_item(
    item_id: int,  # ID of the item to be updated
    item: Item,  # New details for the item
    user: BaseUser,  # User details required for updating the item
    importance: Annotated[int, Body()]  # Importance level provided in the request body
):
    """
    Update an existing item with new details.

    Args:
        item_id (int): The ID of the item to be updated.
        item (Item): New details for the item.
        user (BaseUser): User details associated with the item update.
        importance (int): Importance level of the item.

    Returns:
        dict: A summary of the updated item including its ID, new details, user information, and importance level.
    """
    results = {"item_id": item_id, "item": item, "user": user, "importance": importance}
    return results


# Endpoint to retrieve an item with additional parameters
@app.get("/items/{item_id}")
async def read_user_item(
    item_id: str,  # Path parameter: ID of the item to be retrieved
    needy: str,  # Query parameter: Some additional string information
    num1: int = 5,  # Query parameter with default value: First number (default is 5)
    num2: int | None = 10  # Query parameter with default value: Second number (default is 10, can be None)
):
    """
    Retrieve an item and calculate the sum of two numbers.

    Args:
        item_id (str): The ID of the item to be retrieved.
        needy (str): Additional string information related to the item.
        num1 (int, optional): First number for calculation (default is 5).
        num2 (int or None, optional): Second number for calculation (default is 10, can be None).

    Returns:
        dict: A dictionary containing the item ID, the 'needy' information, and the result of the sum of num1 and num2.
    """
    # Calculate the result based on num1 and num2
    result = (num1 if num1 else 0) + (num2 if num2 else 0)
    
    # Prepare the response with item details and calculation result
    item = {"item_id": item_id, "needy": needy, "result": result}
    return item

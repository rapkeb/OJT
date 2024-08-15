from fastapi.testclient import TestClient
from main import app  # Adjust the import if your FastAPI app is in a different module

client = TestClient(app)

# User-related Tests

def test_create_user_valid():
    response = client.post("/user/", json={
        "username": "testuser",
        "email": "test@example.com",
        "full_name": "Test User",
        "password": "securepassword"
    })
    assert response.status_code == 200
    assert response.json() == {
        "username": "testuser",
        "email": "test@example.com",
        "full_name": "Test User"
    }

def test_create_user_missing_password():
    response = client.post("/user/", json={
        "username": "testuser",
        "email": "test@example.com",
        "full_name": "Test User"
        # Missing 'password'
    })
    assert response.status_code == 422  # Unprocessable Entity

def test_create_user_invalid_email():
    response = client.post("/user/", json={
        "username": "testuser",
        "email": "invalid-email",
        "full_name": "Test User",
        "password": "securepassword"
    })
    assert response.status_code == 422  # Unprocessable Entity

def test_create_user_missing_fields():
    response = client.post("/user/", json={
        "username": "testuser",
        "email": "test@example.com",
        # Missing 'password'
    })
    assert response.status_code == 422

# Video-related Tests

def test_update_event_with_videos():
    response = client.put("/events/1", json={
        "name": "Annual Tech Conference",
        "description": "A conference showcasing the latest in technology and innovation.",
        "tags": ["technology", "conference", "innovation"],
        "videos": [
            {
                "url": "https://www.example.com/video1",
                "name": "Keynote Presentation"
            },
            {
                "url": "https://www.example.com/video2",
                "name": "Tech Panel Discussion"
            }
        ]
    })
    assert response.status_code == 200
    assert response.json() == {
        "event_id": 1,
        "event_name": "Annual Tech Conference",
        "event_tags": ["technology", "conference", "innovation"],
        "videos": "There are videos for the event"
    }

def test_update_event_without_videos():
    response = client.put("/events/2", json={
        "name": "Annual Tech Conference",
        "description": "A conference showcasing the latest in technology and innovation.",
        "tags": ["technology", "conference", "innovation"]
    })
    assert response.status_code == 200
    assert response.json() == {
        "event_id": 2,
        "event_name": "Annual Tech Conference",
        "event_tags": ["technology", "conference", "innovation"],
        "videos": "No videos"
    }

def test_update_event_incorrect_tags_format():
    response = client.put("/events/3", json={
        "name": "Annual Tech Conference",
        "description": "A conference showcasing the latest in technology and innovation.",
        "tags": "technology, conference, innovation"  # Incorrect format, should be a list
    })
    assert response.status_code == 422

def test_update_event_invalid_video_url():
    response = client.put("/events/4", json={
        "name": "Annual Tech Conference",
        "description": "A conference showcasing the latest in technology and innovation.",
        "tags": ["technology", "conference", "innovation"],
        "videos": [
            {
                "url": "invalid-url",
                "name": "Keynote Presentation"
            }
        ]
    })
    assert response.status_code == 422

def test_update_event_missing_optional_fields():
    response = client.put("/events/5", json={
        "name": "Annual Tech Conference",
        "tags": ["technology"]
    })
    assert response.status_code == 200
    assert response.json() == {
        "event_id": 5,
        "event_name": "Annual Tech Conference",
        "event_tags": ["technology"],
        "videos": "No videos"
    }

def test_update_item_valid():
    response = client.put("/items/1", json={
        "item": {
            "name": "Foo",
            "description": "The pretender",
            "price": 42.0,
            "tax": 3.2
        },
        "user": {
            "username": "dave",
            "email": "dave@example.com",
            "full_name": "Dave Grohl"
        },
        "importance": 5
    })
    assert response.status_code == 200
    assert response.json() == {
        "item_id": 1,
        "item": {
            "name": "Foo",
            "description": "The pretender",
            "price": 42.0,
            "tax": 3.2
        },
        "user": {
            "username": "dave",
            "email": "dave@example.com",
            "full_name": "Dave Grohl"
        },
        "importance": 5
    }

def test_update_item_missing_optional_field():
    response = client.put("/items/2", json={
        "item": {
            "name": "Foo",
            "description": "The pretender",
            "price": 42.0
            # 'tax' is omitted
        },
        "user": {
            "username": "dave",
            "email": "dave@example.com",
            "full_name": "Dave Grohl"
        },
        "importance": 5
    })
    assert response.status_code == 200
    assert response.json() == {
        "item_id": 2,
        "item": {
            "name": "Foo",
            "description": "The pretender",
            "price": 42.0,
            "tax": 12.5  # tax should be None when not provided
        },
        "user": {
            "username": "dave",
            "email": "dave@example.com",
            "full_name": "Dave Grohl"
        },
        "importance": 5
    }

def test_update_item_missing_required_fields():
    response = client.put("/items/3", json={
        "item": {
            "name": "Foo",
            # Missing 'price' field
        },
        "user": {
            "username": "dave",
            "email": "dave@example.com",
            "full_name": "Dave Grohl"
        },
        "importance": 5
    })
    assert response.status_code == 422  # Unprocessable Entity

def test_read_user_item():
    # Test case 1: Default values for num1 and num2
    response = client.get("/items/test_item?needy=test&num1=3&num2=4")
    assert response.status_code == 200
    assert response.json() == {"item_id": "test_item", "needy": "test", "result": 7}

    # Test case 2: Using default values for num1 and num2
    response = client.get("/items/test_item?needy=test")
    assert response.status_code == 200
    assert response.json() == {"item_id": "test_item", "needy": "test", "result": 15}

    # Test case 3: num1 provided, num2 not provided (default to None)
    response = client.get("/items/test_item?needy=test&num1=8")
    assert response.status_code == 200
    assert response.json() == {"item_id": "test_item", "needy": "test", "result": 18}
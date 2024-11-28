# FastAPI Receipt Processing Application

This project uses FastAPI to handle API endpoints for processing receipts and calculating points. Data storage is managed using an in-memory database defined in `db/db.py`.

## Architecture

The application follows a Model-Controller-Service-Repository architecture with two models:

- **Receipt** ([`entities.Receipt`](entities/Receipt.py))
- **Item** ([`entities.Item`](entities/Item.py))

The `id` for receipts is generated using Python's `uuid` library.

## Initial Setup

1. **Create a virtual environment:**

    ```sh
    python -m venv venv
    ```

2. **Activate the virtual environment:**

    On Windows:
    ```sh
    venv\Scripts\activate
    ```

    On macOS/Linux:
    ```sh
    source venv/bin/activate
    ```

3. **Install all dependencies:**

    ```sh
    pip install -r requirements.txt
    ```

4. **Run the application:**

    In the root directory, run:
    ```sh
    uvicorn main:app --reload
    ```

## Testing APIs

You can test the APIs using Postman or any other API testing tool.

1. **Create a Receipt**

    Send a POST request to:
    ```
    http://127.0.0.1:8000/receipts/process
    ```

    with JSON formatted data:

    Example:
    ```json
    {
      "retailer": "Target",
      "purchaseDate": "2022-01-01",
      "purchaseTime": "13:01",
      "items": [
         {
            "shortDescription": "Mountain Dew 12PK",
            "price": 6.49
         },
         {
            "shortDescription": "Emils Cheese Pizza",
            "price": 12.25
         },
         {
            "shortDescription": "Knorr Creamy Chicken",
            "price": 1.26
         },
         {
            "shortDescription": "Doritos Nacho Cheese",
            "price": 3.35
         },
         {
            "shortDescription": "   Klarbrunn 12-PK 12 FL OZ  ",
            "price": 12.00
         }
      ],
      "total": 35.35
    }
    ```

    Get the id from the response of the server.

2. **Get Points for a Receipt**

    After obtaining the id, send a GET request to:
    ```
    http://127.0.0.1:8000/receipts/{id}/points
    ```

## Running Tests

To run the tests, execute the following command:
```sh
pytest tests/test_receipts.py
```

This will run the test cases defined to ensure the endpoints are working as expected.
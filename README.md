# Receipt Processor Challenge Solution

This is a Django-based REST API solution using Django REST Framework to process receipts and calculate points based on specific rules.

## Project Approach

1. The models in this project, Receipt and Item, are declared to store the information.
2. Serializers: The two serializers for the above-mentioned models handle data validation and calculation of reward points.
3. Views: The two endpoints - `process_receipt()` and `get_points()` in [views.py](/receipt_processor/receipts/views.py) process receipts and calculate points respectively.

## Tech Stack

- Python
- Django
- Swagger UI
- Django REST Framework
- Docker
- Uses in-memory SQLite database (initialized upon Docker container startup)

## How to run the project (with Docker)

1. Clone the repository

```bash
git clone https://github.com/shahparshva72/receipt-processor-challenge.git
```

2. Navigate to the project directory

```bash
cd receipt-processor-challenge
```

3. Run the docker compose file

```bash
docker-compose up --build
```

4. The project will be available at [http://localhost:8000/](http://localhost:8000/)

## Testing

To run the tests from [tests.py](/receipt_processor/receipts/tests.py), run the following command:

```bash
docker-compose run --rm web python manage.py test
```

## Access the API via terminal or Swagger UI

After running the docker compose file, you can access the Swagger API documentation at the following URL: [http://localhost:8000/swagger/](http://localhost:8000/swagger/) and test the API with sample data from [examples](examples).

You can test the API with the following curl commands in the terminal:

1. Create a receipt: `/receipts/process`

```bash
curl -X POST http://localhost:8000/receipts/process \
-H "Content-Type: application/json" \
-d '{
  "retailer": "M&M Corner Market",
  "purchaseDate": "2022-03-20",
  "purchaseTime": "14:33",
  "items": [
    {
      "shortDescription": "Gatorade",
      "price": "2.25"
    },
    {
      "shortDescription": "Gatorade",
      "price": "2.25"
    },
    {
      "shortDescription": "Gatorade",
      "price": "2.25"
    },
    {
      "shortDescription": "Gatorade",
      "price": "2.25"
    }
  ],
  "total": "9.00"
}'
```

The response will be a JSON object with the ID of the receipt.

```bash
{
    "id": "4ddb89a2-9fc8-4a58-a82a-eae9555399b0"
}
```

2. Get points: `/receipts/{receipt_id}/points`

```bash
curl http://localhost:8000/receipts/4ddb89a2-9fc8-4a58-a82a-eae9555399b0/points
```

The response will be a JSON object with the points of the receipt.

```bash
{ "points": 109 }
```

## Screenshots of the curl requests and responses

![Screenshot of the request and response](/screenshots/image.png)

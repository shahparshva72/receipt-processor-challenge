from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status

class ReceiptsTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        # Valid receipt data for testing from README.md, we should get 109 points.
        self.valid_receipt = {
            "retailer": "M&M Corner Market",
            "purchaseDate": "2022-03-20",
            "purchaseTime": "14:33",
            "items": [
                {"shortDescription": "Gatorade", "price": "2.25"},
                {"shortDescription": "Gatorade", "price": "2.25"},
                {"shortDescription": "Gatorade", "price": "2.25"},
                {"shortDescription": "Gatorade", "price": "2.25"},
            ],
            "total": "9.00",
        }

    def test_create_receipt(self):
        response = self.client.post(
            "/receipts/process", self.valid_receipt, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("id", response.data)

    def test_get_points(self):
        response = self.client.post(
            "/receipts/process", self.valid_receipt, format="json"
        )

        receipt_id = response.data["id"]

        response = self.client.get(f"/receipts/{receipt_id}/points")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("points", response.data)
        self.assertEqual(response.data["points"], 109)

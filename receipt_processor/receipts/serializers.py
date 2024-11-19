from rest_framework import serializers
from .models import Receipt, Item


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ["shortDescription", "price"]
        
    shortDescription = serializers.RegexField(
        regex=r"^[\w\s\-]+$", required=True, source="short_description"
    )
    price = serializers.RegexField(regex=r"^\d+\.\d{2}$", required=True)


class ReceiptSerializer(serializers.ModelSerializer):
    class Meta:
        model = Receipt
        fields = ["retailer", "purchaseDate", "purchaseTime", "items", "total"]
        
    retailer = serializers.RegexField(regex=r"^[\w\s\-&]+$", required=True)
    purchaseDate = serializers.DateField(required=True, source="purchase_date")
    purchaseTime = serializers.TimeField(required=True, source="purchase_time")
    items = ItemSerializer(many=True)
    total = serializers.RegexField(regex=r"^\d+\.\d{2}$", required=True)

    def create(self, validated_data):
        items_data = validated_data.pop("items")
        receipt = Receipt.objects.create(**validated_data)

        for item_data in items_data:
            Item.objects.create(receipt=receipt, **item_data)

        receipt.points = self.calculate_points(receipt)
        receipt.save()

        return receipt

    def calculate_points(self, receipt):
        """
        Rules for calculating points:
        
        1. One point for every alphanumeric character in the retailer name.
        2. 50 points if the total is a round dollar amount with no cents.
        3. 25 points if the total is a multiple of 0.25.
        4. 5 points for every two items on the receipt.
        5. If the trimmed length of the item description is a multiple of 3, multiply the price by 0.2 and round up to the nearest integer. The result is the number of points earned.
        6. 6 points if the day in the purchase date is odd.
        7. 10 points if the time of purchase is after 2:00pm and before 4:00pm.
        """
        points = 0

        points += sum(c.isalnum() for c in receipt.retailer) # Rule 1

        if float(receipt.total) % 1 == 0: # Rule 2
            points += 50

        if float(receipt.total) % 0.25 == 0: # Rule 3
            points += 25

        points += (receipt.items.count() // 2) * 5 # Rule 4

        # Rule 5
        for item in receipt.items.all():
            if len(item.short_description.strip()) % 3 == 0:
                points += int(float(item.price) * 0.2 + 0.99)

        # Rule 6
        if receipt.purchase_date.day % 2 == 1:
            points += 6

        # Rule 7
        if 14 <= receipt.purchase_time.hour < 16:
            points += 10

        return points
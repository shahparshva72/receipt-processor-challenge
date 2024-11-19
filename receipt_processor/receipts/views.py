from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Receipt
from .serializers import ReceiptSerializer

@swagger_auto_schema(
    method='post',
    request_body=ReceiptSerializer,
    responses={200: 'Returns receipt ID', 400: 'Invalid input'}
)
@api_view(['POST'])
def process_receipt(request):
    """
    Process a receipt and return its ID.
    
    Request body should contain receipt details including retailer, purchaseDate, purchaseTime, items, and total.
    """
    serializer = ReceiptSerializer(data=request.data)
    if serializer.is_valid():
        receipt = serializer.save()
        return Response({'id': str(receipt.id)}, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@swagger_auto_schema(
    method='get',
    responses={200: 'Returns points for receipt', 404: 'Receipt not found'}
)
@api_view(['GET'])
def get_points(request, id):
    """
    Get points for a receipt by ID.
    
    Returns the points calculated for the given receipt ID.
    """
    try:
        receipt = Receipt.objects.get(id=id)
        return Response({'points': receipt.points})
    except Receipt.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
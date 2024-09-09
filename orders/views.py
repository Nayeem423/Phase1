# views.py in the orders app

from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from .models import Order, Transaction
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Order, Transaction
from .serializers import OrderSerializer, TransactionSerializer, UserSerializer
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
import pdfkit

def cancel_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    if request.method == 'POST':
        if order.status == 'Pending':
            refund_amount = order.advance_payment * 0.95  # Retain 5% of the advance
            Transaction.objects.create(order=order, amount=refund_amount, transaction_type='Refund')
            order.status = 'Cancelled'
            order.save()
            return JsonResponse({'message': 'Order cancelled, refund processed.'})
        return JsonResponse({'message': 'Order cannot be cancelled after delivery.'}, status=400)

@api_view(['POST'])
@permission_classes([AllowAny])
def customer_login(request):
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(username=username, password=password)
    if user:
        login(request, user)
        refresh = RefreshToken.for_user(user)
        return Response({'refresh': str(refresh), 'access': str(refresh.access_token)}, status=status.HTTP_200_OK)
    return Response({'detail': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def customer_logout(request):
    logout(request)
    return Response({'detail': 'Successfully logged out'}, status=status.HTTP_200_OK)


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def manage_order(request, order_id=None):
    if request.method == 'GET':
        if order_id:
            order = Order.objects.get(pk=order_id)
            serializer = OrderSerializer(order)
        else:
            orders = Order.objects.all()
            serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def track_payments(request, order_id):
    payments = Transaction.objects.filter(order_id=order_id)
    serializer = TransactionSerializer(payments, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def fetch_invoice(request, invoice_id):
    # Here, you'd generate the PDF for the invoice
    # For simplicity, this example just returns a sample response
    pdf_content = "PDF content for invoice {}".format(invoice_id)
    response = HttpResponse(pdf_content, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="invoice_{}.pdf"'.format(invoice_id)
    return response

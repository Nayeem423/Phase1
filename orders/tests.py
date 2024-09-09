# tests.py in the orders app

from rest_framework.test import APITestCase
from rest_framework import status

class OrderTests(APITestCase):
    def test_login(self):
        response = self.client.post('/api/customer/login', {'username': 'user', 'password': 'pass'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_order_creation(self):
        self.client.login(username='user', password='pass')
        response = self.client.post('/api/order', {'client_name': 'Client A', 'advance_payment': 100.00})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

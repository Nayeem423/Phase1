# urls.py in the orders app

from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from . import views

urlpatterns = [
    path('api/customer/login', views.customer_login, name='customer_login'),
    path('api/customer/logout', views.customer_logout, name='customer_logout'),
    path('api/order', views.manage_order, name='manage_order'),
    path('api/order/<int:order_id>', views.manage_order, name='manage_order_by_id'),
    path('api/order/<int:order_id>/payments', views.track_payments, name='track_payments'),
    path('api/order/invoice/<int:invoice_id>', views.fetch_invoice, name='fetch_invoice'),
    path('login/', TemplateView.as_view(template_name='login.html'), name='login'),
    path('orders/', TemplateView.as_view(template_name='orders.html'), name='orders'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


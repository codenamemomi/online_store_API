from django.urls import path
from orders.views import PlaceOrderView, OrderView, OrderViewDetail


urlpatterns = [
    path('place_order/', PlaceOrderView.as_view(), name='place_order'),
    path('order/', OrderView.as_view(), name='order'),
    path('order/<int:order_id>/', OrderViewDetail.as_view(), name='order_detail'),
]
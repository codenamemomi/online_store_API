from django.urls import path
from cart.views import AddToCartView, CartView

urlpatterns =[
    path('cart/', AddToCartView.as_view(), name='cart'),
    path('cart/detail/', CartView.as_view(), name='cart_detail'),
]
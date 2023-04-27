from django.urls import path

from . import views

urlpatterns = [
    # path('cart_item_api/', views.CartItemAPI.as_view(), name='cart_item_api'),
    # # path('cart_item_api/<int:cart_item_id>/', views.CartItemAPI.as_view(), name='cart_item_api'),
    # path('checkout_api/', views.CheckoutAPI.as_view(), name='checkout_api'),
    path('cart_item_api/', views.CheckoutAPI.as_view(), name='cart_item_api'),
]

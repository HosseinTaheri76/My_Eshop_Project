from django.urls import path
from . import views
urlpatterns = [
    path('cart/', views.CartPageView.as_view(), name='cart'),
    path('add_to_cart/<int:product_id>/', views.AddProductToCart.as_view(), name='add_to_cart'),
    path('change_order_item/<str:action>/<int:item_id>/', views.ChangeOrderItem.as_view(), name='change_order_item'),
    path('order_form_register/', views.OrderFormViewRegister.as_view(), name='register_on_order'),
    path('order_form_user/', views.OrderFormAuthenticated.as_view(), name='user_order_form'),
    path('user_orders/', views.UserOrderListView.as_view(), name='user_orders'),
    path('user_orders/<int:order_id>/', views.UserOrderDetail.as_view(), name='user_order_detail'),
]
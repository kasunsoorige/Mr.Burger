from django.urls import path
from .import views

urlpatterns = [
    path('', views.item_list, name='item_list'),
    path('login', views.home, name='home'),
    path('dash',views.dash,name='dash'),
    path('add_menu', views.add_menu, name='add_menu'),
    path('add-to-cart/<int:item_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.view_cart, name='view_cart'),
    path('update-cart/', views.update_cart, name='update_cart'),
    path('remove-from-cart/', views.remove_from_cart, name='remove_from_cart'),
    path('place_order/', views.place_order, name='place_order'),
    path('order-success/', views.order_success, name='order_success'),

]    
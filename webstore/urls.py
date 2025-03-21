from django.urls import path
from .import views
from .views import view_orders
from .views import admin_notifications, mark_notification_read
from .views import order_details
from .views import  delete_order

urlpatterns = [
    path('', views.item_list, name='item_list'),
    path('', views.home, name='home'),
    path('dash',views.dash,name='dash'),
    path('add_menu', views.add_menu, name='add_menu'),
    path('add-to-cart/<int:item_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.view_cart, name='view_cart'),
    path('update-cart/', views.update_cart, name='update_cart'),
    path('remove-from-cart/', views.remove_from_cart, name='remove_from_cart'),
    path('place_order/', views.place_order, name='place_order'),
    path('order-success/', views.order_success, name='order_success'),
    path('manage_menu/', views.manage_menu, name='manage_menu'),
    path('edit_menu/<int:item_id>/', views.edit_menu, name='edit_menu'),
    path('delete_menu/<int:item_id>/', views.delete_menu, name='delete_menu'),

    path('dashboard/orders', views.view_orders, name='view_orders'),  # Correct URL pattern
    path('dashboard/orders/update/<int:order_id>/', views.update_order_status, name='update_order_status'),
    path('my-orders/', views.my_orders, name='my_orders'),
    path('book_table/', views.book_table, name='book_table'),
    path('item_list/', views.item_list, name='item_list'),
    path('reservations/', views.view_reservations, name='view_reservations'),
    path('customer-details/', views.customer_details_form, name='customer_details_form'),
    path('reservation-success/', views.reservation_success, name='reservation_success'),


    path("admin-notifications/", admin_notifications, name="admin_notifications"),
    path("mark-notification-read/<int:notification_id>/", mark_notification_read, name="mark_notification_read"),
    path('order/<int:order_id>/', order_details, name='order_details'),
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('logout/', views.logout_view, name='logout'),



    path('order/cancel/confirm/<int:order_id>/', views.confirm_cancel, name='confirm_cancel'),
    path('order/delete/<int:order_id>/', views.delete_order, name='delete_order'),

    path('rewards/', views.rewards, name='rewards'),

    path('about/', views.about, name='about'),

]    
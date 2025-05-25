from django.urls import path
from . import views

urlpatterns = [
    path('', views.order_list, name='order_list'),
    path('create/', views.order_create, name='order_create'),
    path('delete/<int:order_id>/', views.order_delete, name='order_delete'),
    path('update-status/<int:order_id>/', views.order_update_status, name='order_update_status'),
    
    # API endpoints
    path('api/orders/', views.orders_api_list, name='orders_api_list'),
    path('api/orders/<int:order_id>/', views.orders_api_detail, name='orders_api_detail'),
    path('api/menu/', views.menu_list_api, name='menu_list_api'),
    path('api/revenue/', views.revenue_api, name='revenue_api'),
    path('api/statistics/', views.statistics_api, name='statistics_api'),
]

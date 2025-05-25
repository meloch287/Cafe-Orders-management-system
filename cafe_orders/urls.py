from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from orders import views as orders_views

urlpatterns = [
    path('', lambda request: redirect('order_list', permanent=False)),
    path('admin/', admin.site.urls),
    path('orders/', include('orders.urls')),
    
    # API endpoints на корневом уровне
    path('api/orders/', orders_views.orders_api_list, name='api_orders_list'),
    path('api/orders/<int:order_id>/', orders_views.orders_api_detail, name='api_orders_detail'),
    path('api/menu/', orders_views.menu_list_api, name='api_menu_list'),
    path('api/revenue/', orders_views.revenue_api, name='api_revenue'),
    path('api/statistics/', orders_views.statistics_api, name='api_statistics'),
]

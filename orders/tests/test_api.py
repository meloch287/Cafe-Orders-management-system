from django.test import TestCase, Client
from django.urls import reverse
from rest_framework.test import APIClient
from orders.models import Order, MenuItem
import json
from decimal import Decimal

class APITestCase(TestCase):
    """Тесты для API"""
    
    def setUp(self):
        """Настройка тестовых данных"""
        self.client = APIClient()
        
        # Создаем тестовые заказы
        self.order1 = Order.objects.create(
            table_number=1,
            items=[{'name': 'Суп', 'price': 7.50}, {'name': 'Хлеб', 'price': 1.50}],
            status='waiting'
        )
        
        self.order2 = Order.objects.create(
            table_number=2,
            items=[{'name': 'Стейк', 'price': 15.00}, {'name': 'Вино', 'price': 8.00}],
            status='paid'
        )
        
        # Создаем тестовые пункты меню
        self.menu_item1 = MenuItem.objects.create(
            name='Борщ',
            price=Decimal('8.50'),
            category='soup',
            description='Традиционный борщ со сметаной'
        )
        
        self.menu_item2 = MenuItem.objects.create(
            name='Эспрессо',
            price=Decimal('2.50'),
            category='drink',
            description='Крепкий кофе'
        )
        
        # URL для тестирования
        self.orders_api_url = '/api/orders/'
        self.menu_api_url = '/api/menu/'
        self.revenue_api_url = '/api/revenue/'
        self.statistics_api_url = '/api/statistics/'
    
    def test_get_orders_list(self):
        """Тест получения списка заказов через API"""
        response = self.client.get(self.orders_api_url)
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.content)
        self.assertEqual(len(data), 2)
        self.assertEqual(data[0]['table_number'], 1)
        self.assertEqual(data[1]['table_number'], 2)
    
    def test_get_orders_with_filters(self):
        """Тест получения списка заказов с фильтрами через API"""
        # Фильтр по номеру стола
        response = self.client.get(f"{self.orders_api_url}?table_number=1")
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.content)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['table_number'], 1)
        
        # Фильтр по статусу
        response = self.client.get(f"{self.orders_api_url}?status=paid")
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.content)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['status'], 'paid')
    
    def test_create_order(self):
        """Тест создания заказа через API"""
        new_order_data = {
            'table_number': 3,
            'items': [
                {'name': 'Пицца', 'price': 12.00},
                {'name': 'Сок', 'price': 3.50}
            ]
        }
        
        response = self.client.post(
            self.orders_api_url,
            data=json.dumps(new_order_data),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 201)  # Created
        
        # Проверяем, что заказ был создан
        self.assertEqual(Order.objects.count(), 3)
        new_order = Order.objects.get(table_number=3)
        self.assertEqual(len(new_order.items), 2)
        self.assertEqual(new_order.status, 'waiting')
    
    def test_update_order_status(self):
        """Тест обновления статуса заказа через API"""
        update_data = {'status': 'ready'}
        
        response = self.client.patch(
            f"{self.orders_api_url}{self.order1.id}/",
            data=json.dumps(update_data),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 200)
        
        # Проверяем, что статус был обновлен
        updated_order = Order.objects.get(id=self.order1.id)
        self.assertEqual(updated_order.status, 'ready')
    
    def test_delete_order(self):
        """Тест удаления заказа через API"""
        response = self.client.delete(f"{self.orders_api_url}{self.order1.id}/")
        self.assertEqual(response.status_code, 204)  # No Content
        
        # Проверяем, что заказ был удален
        self.assertEqual(Order.objects.count(), 1)
        self.assertFalse(Order.objects.filter(id=self.order1.id).exists())
    
    def test_get_menu(self):
        """Тест получения меню через API"""
        response = self.client.get(self.menu_api_url)
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.content)
        self.assertEqual(len(data), 2)
        self.assertEqual(data[0]['name'], 'Борщ')
        self.assertEqual(data[1]['name'], 'Эспрессо')
    
    def test_calculate_revenue(self):
        """Тест расчета выручки через API"""
        response = self.client.get(self.revenue_api_url)
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.content)
        self.assertIn('revenue', data)
        self.assertEqual(data['revenue'], 23.0)  # 15.00 + 8.00 = 23.00
    
    def test_get_statistics(self):
        """Тест получения статистики через API"""
        response = self.client.get(self.statistics_api_url)
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.content)
        self.assertIn('status_counts', data)
        self.assertIn('total_orders', data)
        self.assertIn('average_order_value', data)
        
        self.assertEqual(data['total_orders'], 2)
        self.assertEqual(data['status_counts']['waiting'], 1)
        self.assertEqual(data['status_counts']['paid'], 1)

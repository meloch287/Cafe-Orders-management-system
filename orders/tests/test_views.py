from django.test import TestCase, Client
from django.urls import reverse
from orders.models import Order
import json

class OrderViewsTest(TestCase):
    """Тесты для представлений заказов"""
    
    def setUp(self):
        """Настройка тестовых данных"""
        self.client = Client()
        self.order_data = {
            'table_number': 5,
            'items': [
                {'name': 'Суп', 'price': 7.50},
                {'name': 'Кофе', 'price': 2.30}
            ],
            'status': 'waiting'
        }
        self.order = Order.objects.create(**self.order_data)
        
        # URL для тестирования
        self.list_url = reverse('order_list')
        self.create_url = reverse('order_create')
        self.delete_url = reverse('order_delete', args=[self.order.id])
        self.update_status_url = reverse('order_update_status', args=[self.order.id])
    
    def test_order_list_view(self):
        """Тест представления списка заказов"""
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'orders/order_list.html')
        self.assertContains(response, 'Список заказов')
        self.assertContains(response, 'Стол №5')
        
    def test_order_list_view_with_filters(self):
        """Тест представления списка заказов с фильтрами"""
        # Создаем дополнительные заказы для тестирования фильтров
        Order.objects.create(table_number=3, items=[], status='ready')
        Order.objects.create(table_number=5, items=[], status='paid')
        
        # Тест фильтра по номеру стола
        response = self.client.get(f"{self.list_url}?table_number=5")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['orders']), 2)
        
        # Тест фильтра по статусу
        response = self.client.get(f"{self.list_url}?status=waiting")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['orders']), 1)
        
        # Тест комбинированного фильтра
        response = self.client.get(f"{self.list_url}?table_number=5&status=paid")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['orders']), 1)
    
    def test_order_create_view_get(self):
        """Тест GET-запроса к представлению создания заказа"""
        response = self.client.get(self.create_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'orders/order_form.html')
        self.assertContains(response, 'Создать заказ')
    
    def test_order_create_view_post(self):
        """Тест POST-запроса к представлению создания заказа"""
        new_order_data = {
            'table_number': 7,
            'items': json.dumps([
                {'name': 'Пицца', 'price': 12.00},
                {'name': 'Сок', 'price': 3.50}
            ])
        }
        
        response = self.client.post(self.create_url, new_order_data)
        self.assertEqual(response.status_code, 302)  # Редирект после успешного создания
        
        # Проверяем, что заказ был создан
        self.assertEqual(Order.objects.count(), 2)
        new_order = Order.objects.get(table_number=7)
        self.assertEqual(len(new_order.items), 2)
        self.assertEqual(new_order.status, 'waiting')
    
    def test_order_delete_view_get(self):
        """Тест GET-запроса к представлению удаления заказа"""
        response = self.client.get(self.delete_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'orders/order_confirm_delete.html')
        self.assertContains(response, f'Удаление заказа #{self.order.id}')
    
    def test_order_delete_view_post(self):
        """Тест POST-запроса к представлению удаления заказа"""
        response = self.client.post(self.delete_url)
        self.assertEqual(response.status_code, 302)  # Редирект после успешного удаления
        
        # Проверяем, что заказ был удален
        self.assertEqual(Order.objects.count(), 0)
    
    def test_order_update_status_view_get(self):
        """Тест GET-запроса к представлению обновления статуса заказа"""
        response = self.client.get(self.update_status_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'orders/order_update_status.html')
        
        # Отладочный вывод
        response_content = response.content.decode('utf-8')
        expected_text = f'Изменение статуса заказа #{self.order.id}'
        print(f"Ищем текст: '{expected_text}'")
        print(f"Содержимое ответа (первые 1000 символов): {response_content[:1000]}...")
        
        # Проверка наличия текста напрямую
        self.assertIn(expected_text, response_content)  
    
    def test_order_update_status_view_post(self):
        """Тест POST-запроса к представлению обновления статуса заказа"""
        response = self.client.post(self.update_status_url, {'status': 'ready'})
        self.assertEqual(response.status_code, 302)  # Редирект после успешного обновления
        
        # Проверяем, что статус был обновлен
        updated_order = Order.objects.get(id=self.order.id)
        self.assertEqual(updated_order.status, 'ready')
    
    def test_order_update_status_view_post_invalid(self):
        """Тест POST-запроса с неверным статусом"""
        response = self.client.post(self.update_status_url, {'status': 'invalid_status'})
        self.assertEqual(response.status_code, 200)  # Остаемся на той же странице
        
        # Проверяем, что статус не изменился
        updated_order = Order.objects.get(id=self.order.id)
        self.assertEqual(updated_order.status, 'waiting')

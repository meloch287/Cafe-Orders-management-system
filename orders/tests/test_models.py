import unittest
from django.test import TestCase
from django.urls import reverse
from decimal import Decimal
from orders.models import Order, MenuItem

class OrderModelTest(TestCase):
    """Тесты для модели Order"""
    
    def setUp(self):
        """Настройка тестовых данных"""
        self.order_data = {
            'table_number': 5,
            'items': [
                {'name': 'Суп', 'price': 7.50},
                {'name': 'Кофе', 'price': 2.30}
            ],
            'status': 'waiting'
        }
        self.order = Order.objects.create(**self.order_data)
    
    def test_order_creation(self):
        """Тест создания заказа"""
        self.assertEqual(self.order.table_number, 5)
        self.assertEqual(len(self.order.items), 2)
        self.assertEqual(self.order.status, 'waiting')
        self.assertEqual(self.order.total_price, Decimal('9.80'))
    
    def test_order_string_representation(self):
        """Тест строкового представления заказа"""
        self.assertEqual(str(self.order), f"Order #{self.order.id} for Table 5")
    
    def test_get_items_count(self):
        """Тест метода get_items_count"""
        self.assertEqual(self.order.get_items_count(), 2)
    
    def test_is_empty(self):
        """Тест метода is_empty"""
        self.assertFalse(self.order.is_empty())
        
        empty_order = Order.objects.create(table_number=3, items=[], status='waiting')
        self.assertTrue(empty_order.is_empty())
    
    def test_get_status_badge_class(self):
        """Тест метода get_status_badge_class"""
        self.assertEqual(self.order.get_status_badge_class(), 'bg-warning')
        
        self.order.status = 'ready'
        self.order.save()
        self.assertEqual(self.order.get_status_badge_class(), 'bg-info')
        
        self.order.status = 'paid'
        self.order.save()
        self.assertEqual(self.order.get_status_badge_class(), 'bg-success')
    
    def test_total_price_calculation(self):
        """Тест расчета общей стоимости заказа"""
        # Добавляем еще один элемент
        items = self.order.items
        items.append({'name': 'Салат', 'price': 5.50})
        self.order.items = items
        self.order.save()
        
        self.assertEqual(self.order.total_price, Decimal('15.30'))
        
        # Проверяем пустой заказ
        empty_order = Order.objects.create(table_number=3, items=[], status='waiting')
        self.assertEqual(empty_order.total_price, Decimal('0'))


class MenuItemModelTest(TestCase):
    """Тесты для модели MenuItem"""
    
    def setUp(self):
        """Настройка тестовых данных"""
        self.menu_item = MenuItem.objects.create(
            name='Борщ',
            price=Decimal('8.50'),
            category='soup',
            description='Традиционный борщ со сметаной'
        )
    
    def test_menu_item_creation(self):
        """Тест создания пункта меню"""
        self.assertEqual(self.menu_item.name, 'Борщ')
        self.assertEqual(self.menu_item.price, Decimal('8.50'))
        self.assertEqual(self.menu_item.category, 'soup')
        self.assertEqual(self.menu_item.description, 'Традиционный борщ со сметаной')
        self.assertTrue(self.menu_item.is_available)
    
    def test_menu_item_string_representation(self):
        """Тест строкового представления пункта меню"""
        self.assertEqual(str(self.menu_item), 'Борщ (8.50₽)')
    
    def test_is_popular(self):
        """Тест метода is_popular"""
        # В текущей реализации метод всегда возвращает False
        self.assertFalse(self.menu_item.is_popular())

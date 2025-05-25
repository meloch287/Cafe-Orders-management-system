from django.db import models
from django.utils import timezone
from decimal import Decimal

class Order(models.Model):
    STATUS_CHOICES = [
        ('waiting', 'В ожидании'),
        ('ready', 'Готово'),
        ('paid', 'Оплачено'),
    ]
    
    table_number = models.PositiveIntegerField()
    # Сохраняем список блюд в формате JSON (каждый элемент: словарь с 'name' и 'price')
    items = models.JSONField(default=list)
    total_price = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='waiting')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['status']),
            models.Index(fields=['table_number']),
            models.Index(fields=['created_at']),
        ]
    
    def save(self, *args, **kwargs):
        # Рассчитываем общую стоимость заказа только если items изменились
        # или это новый объект
        if not self.pk or 'items' in kwargs.get('update_fields', ['items']):
            self.total_price = sum(Decimal(str(item.get('price', 0))) for item in self.items)
        super().save(*args, **kwargs)
    
    def get_items_count(self):
        """Возвращает количество позиций в заказе"""
        return len(self.items)
    
    def is_empty(self):
        """Проверяет, пуст ли заказ"""
        return len(self.items) == 0
    
    def get_status_badge_class(self):
        """Возвращает класс для отображения статуса"""
        status_classes = {
            'waiting': 'bg-warning',
            'ready': 'bg-info',
            'paid': 'bg-success',
        }
        return status_classes.get(self.status, 'bg-secondary')
        
    def __str__(self):
        return f"Order #{self.id} for Table {self.table_number}"


class MenuItem(models.Model):
    CATEGORY_CHOICES = [
        ('snack', 'Закуски'),
        ('main', 'Основные блюда'),
        ('soup', 'Супы'),
        ('salad', 'Салаты'),
        ('dessert', 'Десерты'),
        ('drink', 'Напитки'),
    ]
    
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    description = models.TextField(blank=True)
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['category', 'name']
        indexes = [
            models.Index(fields=['category']),
            models.Index(fields=['is_available']),
        ]
    
    def is_popular(self):
        """Метод для определения популярности блюда (заглушка)"""
        # В реальном приложении здесь была бы логика определения популярности
        return False
    
    def __str__(self):
        return f"{self.name} ({self.price}₽)"

from django import forms
from .models import Order, MenuItem
import re
import json

class OrderTemplateForm(forms.Form):
    """Форма для выбора шаблона заказа"""
    template = forms.ModelChoiceField(
        queryset=MenuItem.objects.filter(is_available=True),
        required=False,
        empty_label="Выберите шаблон заказа",
        label="Шаблон заказа"
    )

class OrderForm(forms.ModelForm):
    """Форма для создания и редактирования заказа"""
    # Оригинальное поле items для совместимости с тестами
    items = forms.CharField(
        widget=forms.Textarea(attrs={
            'rows': 5,
            'placeholder': '[{"name": "Название блюда 1", "price": цена1}, {"name": "Название блюда 2", "price": цена2}]',
            'id': 'id_items'
        }),
        required=False,
        label="Блюда (JSON формат)"
    )
    
    # Текстовое поле для ввода блюд в формате "название - цена"
    items_text = forms.CharField(
        widget=forms.Textarea(attrs={
            'rows': 5,
            'placeholder': 'Введите блюда в формате "название - цена" (по одному на строку)\nПример:\nСуп - 250\nКофе - 150'
        }),
        required=False,
        label="Блюда (текстовый ввод)"
    )
    
    # Поле для выбора готовых блюд из меню
    menu_items = forms.ModelMultipleChoiceField(
        queryset=MenuItem.objects.filter(is_available=True),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="Выберите из меню"
    )

    class Meta:
        model = Order
        fields = ['table_number', 'items']
        labels = {
            'table_number': 'Номер стола',
            'items': 'Блюда (JSON формат)',
        }
        widgets = {
            'table_number': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
        }

    def clean(self):
        cleaned_data = super().clean()
        items_text = cleaned_data.get('items_text', '')
        items_json = cleaned_data.get('items', '')
        menu_items = cleaned_data.get('menu_items', [])
        
        items = []
        
        # Обработка текстового ввода
        if items_text:
            lines = items_text.strip().split('\n')
            for line in lines:
                if not line.strip():
                    continue
                    
                # Парсим строку в формате "название - цена"
                match = re.match(r'(.+?)\s*-\s*(\d+(?:\.\d+)?)', line)
                if match:
                    name = match.group(1).strip()
                    try:
                        price = float(match.group(2))
                        items.append({"name": name, "price": price})
                    except ValueError:
                        self.add_error('items_text', f'Некорректная цена в строке: "{line}"')
                else:
                    self.add_error('items_text', f'Некорректный формат в строке: "{line}". Используйте формат "название - цена"')
        
        # Обработка JSON-ввода
        if items_json:
            try:
                json_items = json.loads(items_json)
                if isinstance(json_items, list):
                    for item in json_items:
                        if isinstance(item, dict) and 'name' in item and 'price' in item:
                            name = item['name']
                            try:
                                price = float(item['price'])
                                items.append({"name": name, "price": price})
                            except (ValueError, TypeError):
                                self.add_error('items', f'Некорректная цена для блюда "{name}"')
                        else:
                            self.add_error('items', 'Каждый элемент должен содержать поля "name" и "price"')
                else:
                    self.add_error('items', 'JSON должен быть списком объектов')
            except json.JSONDecodeError:
                self.add_error('items', 'Некорректный JSON формат')
        
        # Обработка выбранных элементов меню
        if menu_items:
            for item in menu_items:
                items.append({"name": item.name, "price": float(item.price)})
        
        # Проверяем, что хотя бы один способ ввода был использован
        if not items:
            self.add_error(None, 'Добавьте хотя бы одно блюдо через любой из способов ввода')
        
        cleaned_data['items'] = items
        return cleaned_data

    def save(self, commit=True):
        instance = super(OrderForm, self).save(commit=False)
        instance.items = self.cleaned_data.get('items', [])
        
        if commit:
            instance.save()
        return instance

class OrderTemplateForm(forms.ModelForm):
    """Форма для создания шаблонов заказов в админке"""
    class Meta:
        model = MenuItem
        fields = ['name', 'price', 'category', 'description', 'is_available']
        labels = {
            'name': 'Название',
            'price': 'Цена',
            'category': 'Категория',
            'description': 'Описание',
            'is_available': 'Доступно',
        }

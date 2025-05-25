// Обновленный JavaScript для предотвращения дублирования блюд
document.addEventListener('DOMContentLoaded', function() {
  // Обработчик добавления шаблона заказа
  document.getElementById('addTemplateBtn').addEventListener('click', function() {
    const templateSelect = document.getElementById('orderTemplate');
    const selectedOption = templateSelect.options[templateSelect.selectedIndex];
    
    if (templateSelect.value) {
      const name = selectedOption.getAttribute('data-name');
      const price = parseFloat(selectedOption.getAttribute('data-price'));
      
      // Проверяем, не добавлено ли уже это блюдо
      const textArea = document.getElementById('{{ form.items_text.id_for_label }}');
      const lines = textArea.value.split('\n').filter(line => line.trim() !== '');
      
      // Проверяем, есть ли уже такое блюдо с такой ценой
      const isDuplicate = lines.some(line => {
        const match = line.match(/(.+?)\s*-\s*(\d+(?:\.\d+)?)/);
        if (match) {
          const existingName = match[1].trim();
          const existingPrice = parseFloat(match[2]);
          return existingName === name && existingPrice === price;
        }
        return false;
      });
      
      // Добавляем только если это не дубликат
      if (!isDuplicate) {
        if (lines.length > 0) {
          textArea.value += '\n';
        }
        textArea.value += `${name} - ${price}`;
        
        // Обновляем предпросмотр
        updateOrderPreview();
        
        // Обновляем скрытое поле items для совместимости с тестами
        updateItemsField();
      }
    }
  });
  
  // Функция обновления предпросмотра заказа
  function updateOrderPreview() {
    const previewTable = document.getElementById('orderPreviewTable').getElementsByTagName('tbody')[0];
    const totalElement = document.getElementById('orderTotal');
    let items = [];
    let total = 0;
    
    // Очищаем таблицу
    previewTable.innerHTML = '';
    
    // Создаем объект для отслеживания уникальности блюд
    const uniqueItems = {};
    
    // Собираем данные из текстового поля
    const textArea = document.getElementById('{{ form.items_text.id_for_label }}');
    if (textArea.value) {
      const lines = textArea.value.split('\n');
      for (const line of lines) {
        const match = line.match(/(.+?)\s*-\s*(\d+(?:\.\d+)?)/);
        if (match) {
          const name = match[1].trim();
          const price = parseFloat(match[2]);
          const key = `${name}-${price}`;
          
          // Добавляем только если это уникальное блюдо
          if (!uniqueItems[key]) {
            uniqueItems[key] = { name, price };
          }
        }
      }
    }
    
    // Собираем данные из чекбоксов меню
    const checkboxes = document.querySelectorAll('input[name="{{ form.menu_items.name }}"]');
    for (const checkbox of checkboxes) {
      if (checkbox.checked) {
        const label = checkbox.parentElement.textContent.trim();
        const match = label.match(/(.+?)\s*\((\d+(?:\.\d+)?)₽\)/);
        if (match) {
          const name = match[1].trim();
          const price = parseFloat(match[2]);
          const key = `${name}-${price}`;
          
          // Добавляем только если это уникальное блюдо
          if (!uniqueItems[key]) {
            uniqueItems[key] = { name, price };
          }
        }
      }
    }
    
    // Преобразуем объект уникальных блюд обратно в массив
    items = Object.values(uniqueItems);
    
    // Рассчитываем общую сумму
    total = items.reduce((sum, item) => sum + item.price, 0);
    
    // Заполняем таблицу
    for (const item of items) {
      const row = previewTable.insertRow();
      const nameCell = row.insertCell(0);
      const priceCell = row.insertCell(1);
      
      nameCell.textContent = item.name;
      priceCell.textContent = `${item.price.toFixed(2)}₽`;
      priceCell.className = 'text-end';
    }
    
    // Если нет элементов, показываем сообщение
    if (items.length === 0) {
      const row = previewTable.insertRow();
      const cell = row.insertCell(0);
      cell.colSpan = 2;
      cell.textContent = 'Нет добавленных блюд';
      cell.className = 'text-center text-muted';
    }
    
    // Обновляем итоговую сумму
    totalElement.textContent = `${total.toFixed(2)}₽`;
    
    // Обновляем скрытое поле items для совместимости с тестами
    updateItemsField();
  }
  
  // Функция обновления скрытого поля items для совместимости с тестами
  function updateItemsField() {
    // Создаем объект для отслеживания уникальности блюд
    const uniqueItems = {};
    
    // Собираем данные из текстового поля
    const textArea = document.getElementById('{{ form.items_text.id_for_label }}');
    if (textArea.value) {
      const lines = textArea.value.split('\n');
      for (const line of lines) {
        const match = line.match(/(.+?)\s*-\s*(\d+(?:\.\d+)?)/);
        if (match) {
          const name = match[1].trim();
          const price = parseFloat(match[2]);
          const key = `${name}-${price}`;
          
          // Добавляем только если это уникальное блюдо
          if (!uniqueItems[key]) {
            uniqueItems[key] = { name, price };
          }
        }
      }
    }
    
    // Собираем данные из чекбоксов меню
    const checkboxes = document.querySelectorAll('input[name="{{ form.menu_items.name }}"]');
    for (const checkbox of checkboxes) {
      if (checkbox.checked) {
        const label = checkbox.parentElement.textContent.trim();
        const match = label.match(/(.+?)\s*\((\d+(?:\.\d+)?)₽\)/);
        if (match) {
          const name = match[1].trim();
          const price = parseFloat(match[2]);
          const key = `${name}-${price}`;
          
          // Добавляем только если это уникальное блюдо
          if (!uniqueItems[key]) {
            uniqueItems[key] = { name, price };
          }
        }
      }
    }
    
    // Преобразуем объект уникальных блюд обратно в массив
    const items = Object.values(uniqueItems);
    
    // Обновляем скрытое поле items
    const itemsField = document.getElementById('id_items');
    itemsField.value = JSON.stringify(items);
  }
  
  // Обновляем предпросмотр при изменении любого поля
  document.getElementById('{{ form.items_text.id_for_label }}').addEventListener('input', updateOrderPreview);
  
  const checkboxes = document.querySelectorAll('input[name="{{ form.menu_items.name }}"]');
  for (const checkbox of checkboxes) {
    checkbox.addEventListener('change', updateOrderPreview);
  }
  
  // Инициализируем предпросмотр
  updateOrderPreview();
  
  // Обработчик отправки формы
  document.getElementById('orderForm').addEventListener('submit', function(event) {
    const itemsField = document.getElementById('id_items');
    try {
      const items = JSON.parse(itemsField.value);
      if (items.length === 0) {
        event.preventDefault();
        alert('Пожалуйста, добавьте хотя бы одно блюдо в заказ.');
      }
    } catch (e) {
      event.preventDefault();
      alert('Ошибка в формате данных. Пожалуйста, проверьте ввод.');
    }
  });
});

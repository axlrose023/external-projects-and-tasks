
# Admiral Studios - Django To-Do API

### Опис
Це REST API для управління списком завдань (To-Do) на Django, створене для тестового завдання. API дозволяє переглядати список завдань, додавати нові завдання, оновлювати статус завдання (позначати як виконане) та видаляти завдання.

### Вимоги
- Python 3.13
- Django 5.1.3
- Django REST Framework

### Налаштування проекту

1. Клонуйте репозиторій або завантажте проект.
2. Встановіть залежності:
   ```bash
   pip install -r requirements.txt
   ```
3. Зробіть міграції та запустіть сервер:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   python manage.py runserver
   ```

---

## API Ендпоінти

### 1. Отримати список завдань
**GET /api/tasks/**  
Повертає список усіх завдань, відсортованих за датою створення.

**Приклад відповіді:**
```json
[
    {
        "id": 1,
        "title": "Buy groceries",
        "description": "Milk, Bread, Eggs",
        "is_completed": false,
        "created_at": "2024-11-15T12:00:00Z"
    }
]
```

### 2. Додати нове завдання
**POST /api/tasks/**  
Створює нове завдання.

**Тіло запиту:**
```json
{
    "title": "Read a book",
    "description": "Read 'Clean Code'"
}
```

**Приклад відповіді:**
```json
{
    "id": 2,
    "title": "Read a book",
    "description": "Read 'Clean Code'",
    "is_completed": false,
    "created_at": "2024-11-15T12:30:00Z"
}
```

### 3. Оновити завдання (позначити як виконане)
**PATCH /api/tasks/id/**  
Оновлює статус завдання (позначає як виконане).

**Тіло запиту:**
```json
{
    "is_completed": true
}
```

**Приклад відповіді:**
```json
{
    "id": 1,
    "title": "Buy groceries",
    "description": "Milk, Bread, Eggs",
    "is_completed": true,
    "created_at": "2024-11-15T12:00:00Z"
}
```

### 4. Видалити завдання
**DELETE /api/tasks/id/**  
Видаляє завдання за вказаним `id`.

**Приклад відповіді:**
```
204 No Content
```

---

## Middleware для Логування

Ми використовуємо `RequestLoggingMiddleware` для логування запитів та відповідей.

### Приклад логів у консолі
```
[INFO] [GET] /api/tasks/ - 200 - 0.003s
[INFO] [POST] /api/tasks/ - 201 - 0.005s
[INFO] [PATCH] /api/tasks/1/ - 200 - 0.004s
[INFO] [DELETE] /api/tasks/1/ - 204 - 0.002s
```


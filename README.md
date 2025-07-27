# Медицинский диагностический центр - Веб-сайт

## Установка и запуск

1. Клонировать репозиторий:
```bash
git clone https://github.com/yourusername/medical-diagnostics.git
cd medical-diagnostics
```
2. Создать и активировать виртуальное окружение:
```bash
python -m venv venv
source venv/bin/activate  # Linux/MacOS
venv\Scripts\activate     # Windows
```
3. Установить зависимости:
```bash
pip install -r requirements.txt
```
4. Настройка переменных окружения:
Создать файл .env в корне проекта:
```bash
SECRET_KEY=YOUR_SECRET_KEY
DEBUG=YOUR_DEBUG

NAME=YOUR_NAME
USER=YOUR_USER
PASSWORD=YOUR_PASSWORD
HOST=YOUR_HOST
PORT=PORT
```
5. Запуск с Docker:
```bash
docker-compose up --build
```
6. Миграции и суперпользователь:
```bash
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser
```
Сайт будет доступен по адресу: 
```bash
http://localhost:8000
```
Админка: 
```bash
http://localhost:8000/admin
```
## Дополнительные улучшения

1. **Система записи на прием**:
   - Календарь с доступными датами
   - Выбор врача и услуги
   - Подтверждение по email/SMS

2. **Личный кабинет пациента**:
   - История посещений
   - Результаты анализов (PDF)
   - Возможность отменить запись

3. **Поиск по услугам**:
   - Фильтрация по категориям
   - Поиск по названию

4. **Блог медицинских статей**:
   - Полезная информация для пациентов
   - Категории статей

5. **Онлайн-консультации**:
   - Интеграция с видео-сервисами
   - Чат с врачом

Этот проект предоставляет полную основу для сайта медицинской диагностики с использованием Django и Bootstrap. 
Вы можете расширять и модифицировать его по своему усмотрению.
# Чат бот на основе YandexGPT



Перед началом работы активируйте виртуальную среду:
- source env/bin/activate - для Linux
- .\venv\Scripts\activate - для Windows

Установите:
- pip install -r requirements.txt
___
# Перед запуском бота необходимо ввести свои значения:

- TOKEN_BOT - токен от botfather
- API_KEY - ключ yandexcloud
- FOLDER_ID - id каталога yandexcloud
- REDIS_URL - можно использовать стандартные значения

---
В моем коде используется файл secret.py добавленный в .gitignore, в связи с неисправностью моей конфигурации. Для использования с dotenv и аналогами, предлагаю использовать os.getenv("API_KEY")
___
# Запуск бота

- python3 main.py - для Linux
- python .\main.py - для windows
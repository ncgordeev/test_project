import os
from django.core.management.base import BaseCommand
from mongoengine import connect
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError

class Command(BaseCommand):
    help = 'Test MongoDB connection'

    def handle(self, *args, **options):
        try:
            # Параметры подключения
            db_name = os.getenv("MONGODB_NAME")
            host = os.getenv("MONGODB_HOST")
            port = int(os.getenv("MONGODB_PORT", 27017))
            username = os.getenv("MONGODB_USER")
            password = os.getenv("MONGODB_PASSWORD")

            # Подключение
            connect(
                db=db_name,
                host=host,
                port=port,
                username=username,
                password=password,
                authentication_source='admin'
            )

            # Проверка соединения
            from mongoengine.connection import get_connection
            conn = get_connection()
            conn.admin.command('ping')  # Явная проверка доступности

            self.stdout.write(self.style.SUCCESS("✅ MongoDB connection successful!"))

        except (ConnectionFailure, ServerSelectionTimeoutError) as e:
            self.stdout.write(self.style.ERROR(f"❌ Connection failed: {str(e)}"))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"❌ Unexpected error: {str(e)}"))
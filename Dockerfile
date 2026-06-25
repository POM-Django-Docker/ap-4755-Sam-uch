# Базовий офіційний образ Python (slim — полегшена версія)
FROM python:3.12-slim

# Робоча директорія всередині контейнера
WORKDIR /app

# Копіюємо файл залежностей окремо, щоб Docker кешував цей шар
COPY requirements.txt .

# Встановлюємо залежності
RUN pip install --no-cache-dir -r requirements.txt

# Копіюємо решту коду програми
COPY . .

# Порт, який слухає програма
EXPOSE 8000

# Команда запуску сервера
CMD ["python", "main.py"]

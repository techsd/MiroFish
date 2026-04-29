# Конфігурація (Environment Configuration)

Гнучкість системи MiroFish забезпечується через змінні середовища (Environment Variables) та конфігураційні файли.

## 1. Файл `.env`

Основний файл конфігурації знаходиться в корені проекту. Він не додається до репозиторію (є в `.gitignore`). Шаблон знаходиться в `.env.example`.

### LLM Провайдер
```env
LLM_API_KEY=your_api_key                # Ваш ключ доступу до LLM
LLM_BASE_URL=https://api.openai.com/v1  # Базова URL адреса API (для OpenAI, Ollama, Qwen тощо)
LLM_MODEL_NAME=gpt-4o                   # Назва моделі (наприклад, qwen-plus, llama3)
```

### Zep Конфігурація
```env
ZEP_API_KEY=your_zep_key                # Ключ для Zep Cloud (залиште порожнім або будь-яким для локального Zep)
ZEP_API_URL=http://localhost:8000       # URL локального сервера Zep (лише для Offline-версії)
```

### Системні ліміти та налаштування
```env
MAX_SIMULATION_ROUNDS=100               # Максимально дозволена кількість раундів (захист від перевитрати токенів)
BACKEND_PORT=5001                       # Порт для бекенд-сервера
FRONTEND_PORT=3000                      # Порт для фронтенд-сервера
DEBUG_MODE=false                        # Увімкнення розширеного логування
```

## 2. Конфігурація Frontend (`vite.config.js`)

Файл налаштувань для збирача Vite. Основні параметри, які можна змінити:
- **Port:** Налаштування порту розробки (за замовчуванням `3000`).
- **Proxy:** Налаштування проксі для вирішення проблем з CORS під час локальної розробки. Усі запити, що починаються з `/api`, автоматично перенаправляються на `http://localhost:5001`.

## 3. Конфігурація Backend (`pyproject.toml`)

Файл налаштувань для пакетного менеджера `uv`.
- **dependencies:** Перелік усіх необхідних Python бібліотек та їхніх версій (Flask, oasis, zep-cloud, zep-python, openai тощо).
- **requires-python:** Вказує мінімально підтримувану версію Python (`>=3.11`).

## 4. Конфігурація локалізації (`locales/languages.json`)

Файл управління мовами інтерфейсу:
```json
{
  "en": {
    "label": "English",
    "llmInstruction": "Please respond in English."
  },
  "uk": {
    "label": "Українська",
    "llmInstruction": "Будь ласка, відповідай українською мовою."
  }
}
```
*Примітка:* Параметр `llmInstruction` автоматично додається до промптів Report Agent, щоб фінальний звіт генерувався обраною мовою.

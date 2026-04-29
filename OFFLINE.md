# Гайд з переналаштування MiroFish для 100% Offline режиму (OFFLINE.md)

Цей посібник допоможе розгорнути проект MiroFish у повністю закритому (ізольованому) мережевому середовищі без доступу до інтернету.

## 1. Локальний LLM Провайдер

Для роботи без інтернету вам знадобиться локальний сервер LLM, який підтримує API у форматі OpenAI. Найпопулярніші рішення:

- **LM Studio** (простий UI, для Windows/Mac/Linux)
- **Ollama** (консольний інструмент)
- **vLLM** (для серверів з потужними GPU)

### Налаштування .env для локальної LLM
Після запуску локального сервера (наприклад, LM Studio або Ollama), змініть файл `.env` наступним чином:

Для LM Studio (за замовчуванням порт 1234):
```env
LLM_API_KEY=lm-studio
LLM_BASE_URL=http://127.0.0.1:1234/v1
LLM_MODEL_NAME=local-model
```

Для Ollama (за замовчуванням порт 11434):
```env
LLM_API_KEY=ollama
LLM_BASE_URL=http://127.0.0.1:11434/v1
LLM_MODEL_NAME=llama3
```
*Зверніть увагу: LLM_MODEL_NAME має збігатися з назвою моделі, яка завантажена у ваш локальний сервер.*

## 2. Локальна пам'ять (Zep Server)

В оригінальному проекті жорстко прописана залежність від хмарної версії Zep (`zep-cloud==3.13.0`). Для 100% офлайн режиму вам необхідно підняти локальний Zep сервер та замінити бібліотеку.

### Крок 1: Запуск локального Zep через Docker
```bash
docker run -p 8000:8000 getzep/zep:latest
```

### Крок 2: Зміна залежностей у бекенді
Оскільки `zep-cloud` працює тільки з хмарою, вам потрібно перейти на `zep-python` (Community Edition).
У файлах `backend/requirements.txt` та `backend/pyproject.toml` замініть:
`zep-cloud==3.13.0` на `zep-python`

Встановіть нові залежності:
```bash
cd backend
uv remove zep-cloud
uv add zep-python
```

### Крок 3: Адаптація коду
У всіх файлах в `backend/app/services/` та `backend/app/utils/` вам потрібно буде змінити імпорти:
Замість `from zep_cloud.client import Zep`
Використовувати `from zep_python import ZepClient`

Після цього у `.env` можна буде додати URL вашого локального сервера:
```env
ZEP_API_URL=http://127.0.0.1:8000
ZEP_API_KEY=zep-local-key
```
Також потрібно буде передавати цей `ZEP_API_URL` при ініціалізації клієнта у коді.

## 3. Запуск проекту в Offline середовищі

Якщо ваш комп'ютер повністю відключений від інтернету, переконайтеся, що ви заздалегідь:
1. Завантажили та встановили всі пакети Python (`uv sync`) та Node.js (`npm install`) поки інтернет ще був.
2. Завантажили Docker-образи для Zep та LLM.
3. Завантажили ваги LLM моделей (файли .gguf або .safetensors).

Після цього запуск не відрізняється від звичайного:
```bash
npm run dev
```

Обидва порти (3000 для фронтенду та 5001 для бекенду) працюватимуть через локальну мережу localhost (127.0.0.1) і не потребуватимуть зовнішніх запитів.

## 4. Автоматизація міграції (Zero Config Script)

Щоб не виконувати кроки заміни імпортів Zep та залежностей вручну, ви можете створить файл `offline_migration.py` у корені проекту з наступним кодом:

```python
import os, glob

def migrate_to_offline():
    # 1. Заміна у requirements.txt
    req_path = 'backend/requirements.txt'
    if os.path.exists(req_path):
        content = open(req_path, 'r', encoding='utf-8').read()
        open(req_path, 'w', encoding='utf-8').write(content.replace('zep-cloud==3.13.0', 'zep-python'))
        
    # 2. Заміна у pyproject.toml
    pyproj_path = 'backend/pyproject.toml'
    if os.path.exists(pyproj_path):
        content = open(pyproj_path, 'r', encoding='utf-8').read()
        open(pyproj_path, 'w', encoding='utf-8').write(content.replace('"zep-cloud==3.13.0"', '"zep-python"'))

    # 3. Рекурсивна заміна імпортів у коді
    for py_file in glob.glob('backend/app/**/*.py', recursive=True):
        with open(py_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        if 'zep_cloud' in content:
            # Змінюємо імпорти на локальну версію
            content = content.replace('from zep_cloud.client import Zep', 'from zep_python import ZepClient as Zep')
            content = content.replace('import zep_cloud', 'import zep_python')
            
            with open(py_file, 'w', encoding='utf-8') as f:
                f.write(content)
                
    print("Zero Config міграція для Offline режиму успішно завершена!")
    print("Виконайте: cd backend && uv sync")

if __name__ == '__main__':
    migrate_to_offline()
```

Запустіть цей скрипт однією командою (`python offline_migration.py`), і він автоматично перепише всі необхідні файли для роботи з локальним Zep сервером.

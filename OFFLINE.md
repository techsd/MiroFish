# Гайд з переналаштування MiroFish для 100% Offline режиму

Цей документ описує, як підготувати та налаштувати ключові файли проекту для роботи в повністю ізольованому середовищі без доступу до інтернету.

## 1. Підготовка залежностей (Online етап)

Щоб працювати офлайн, необхідно заздалегідь підготувати залежності, які зазвичай викачуються з інтернету.

- **package.json та package-lock.json**: Містять npm-пакети з `registry.npmjs.org`. В офлайн режимі команди `npm install` або `npm ci` завершаться з помилкою. Вам потрібно виконати `npm ci` поки є інтернет, щоб тека `node_modules` була повністю сформована, і переносити проект разом із цією текою.
- **backend/uv.lock та pyproject.toml**: Містять Python-залежності з `files.pythonhosted.org`. Потрібно виконати `uv sync` онлайн, щоб завантажити все у теку `.venv`. 
- **Ваги моделей LLM**: Завантажте `.gguf` або `.safetensors` файли локальних моделей (наприклад, Llama 3 або Qwen) для їх використання у програмах типу LM Studio або Ollama.

## 2. Налаштування Docker для Offline

Якщо ви плануєте використовувати Docker, пам'ятайте про наступне:

- **Dockerfile**: Цей файл містить команди `apt-get update`, `npm ci`, `uv sync`. Зібрати цей образ на комп'ютері без інтернету неможливо, оскільки він завантажує пакети. Вам потрібно зібрати образ на комп'ютері з інтернетом: `docker build -t mirofish-local .`.
- **docker-compose.yml**: Файл намагається завантажити образ `ghcr.io/666ghj/mirofish:latest` з GitHub Container Registry. Щоб перенести його на офлайн-машину, виконайте на машині з інтернетом:
  `docker pull ghcr.io/666ghj/mirofish:latest`
  `docker save -o mirofish.tar ghcr.io/666ghj/mirofish:latest`
  Потім перенесіть файл `mirofish.tar` на офлайн комп'ютер і виконайте:
  `docker load -i mirofish.tar`
- **.dockerignore**: Файл спеціально ігнорує теки `node_modules` та `.venv`. Якщо ви спробуєте скомпілювати або скопіювати проект всередину контейнера вручну (без збірки Dockerfile), ці залежності будуть проігноровані. Тому образ потрібно переносити саме через `docker save / load`.

## 3. Налаштування змінних середовища (.env)

Файл `.env.example` та ваш робочий `.env` містять посилання на зовнішні API. Для офлайн режиму їх потрібно переналаштувати на локальні сервіси (localhost / 127.0.0.1).

Для LLM (приклад для локального сервера LM Studio на порту 1234):
```env
LLM_API_KEY=local-key
LLM_BASE_URL=http://127.0.0.1:1234/v1
LLM_MODEL_NAME=назва_вашої_локальної_моделі
```

Для системи пам'яті агентів (якщо ви використовуєте локальний Docker-контейнер Zep Community Edition):
```env
ZEP_API_URL=http://127.0.0.1:8000
ZEP_API_KEY=local-zep-key
```

## 4. Файли ігнорування (.gitignore)

Файл `.gitignore` приховує від системи контролю версій `.env`, `node_modules` та `.venv`. Якщо ви переносите проект між комп'ютерами через Git або архівуєте його лише за відслідковуваними файлами, переконайтеся, що ви скопіювали також ці ігноровані файли і теки вручну. Інакше проект не запуститься в офлайн режимі через відсутність залежностей та конфігурації.

## 5. Автоматизація заміни коду Zep

Оригінальний код використовує пакет `zep-cloud`, який працює виключно через інтернет. Для роботи з локальним сервером Zep його треба замінити на `zep-python`.
Створіть файл `offline_migration.py` у корені проекту та запустіть його (`python offline_migration.py`), щоб автоматично оновити імпорти та залежності:

```python
import os, glob

def migrate_to_offline():
    req_path = 'backend/requirements.txt'
    if os.path.exists(req_path):
        content = open(req_path, 'r', encoding='utf-8').read()
        open(req_path, 'w', encoding='utf-8').write(content.replace('zep-cloud==3.13.0', 'zep-python'))
        
    pyproj_path = 'backend/pyproject.toml'
    if os.path.exists(pyproj_path):
        content = open(pyproj_path, 'r', encoding='utf-8').read()
        open(pyproj_path, 'w', encoding='utf-8').write(content.replace('"zep-cloud==3.13.0"', '"zep-python"'))

    for py_file in glob.glob('backend/app/**/*.py', recursive=True):
        with open(py_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        if 'zep_cloud' in content:
            content = content.replace('from zep_cloud.client import Zep', 'from zep_python import ZepClient as Zep')
            content = content.replace('import zep_cloud', 'import zep_python')
            
            with open(py_file, 'w', encoding='utf-8') as f:
                f.write(content)
                
if __name__ == '__main__':
    migrate_to_offline()
    print("Міграцію завершено! Тепер виконайте: cd backend && uv sync")
```

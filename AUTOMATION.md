# Автоматизація та Скрипти (Automation & CI/CD)

Система MiroFish містить набір скриптів для автоматизації процесів налаштування, розгортання та міграції.

## 1. NPM Скрипти (Управління проектом)

У файлі `package.json` кореневої директорії визначено основні команди:

- `npm run setup:all` — Одночасно встановлює залежності для frontend (через `npm`) та backend (через `uv`).
- `npm run setup` — Встановлює лише NPM залежності (кореневі та frontend).
- `npm run setup:backend` — Створює віртуальне середовище Python (`.venv`) та встановлює залежності бекенду через `uv sync`.
- `npm run dev` — Запускає паралельно Frontend-сервер (Vite) та Backend-сервер (Flask).
- `npm run frontend` / `npm run backend` — Запуск окремих сервісів.

## 2. Скрипти обслуговування (Maintenance)

### Міграція в Offline-режим
Скрипт `offline_migration.py` використовується для автоматичної міграції кодової бази на використання локальної версії Zep:
```bash
python offline_migration.py
```
**Що він робить:**
1. Оновлює `requirements.txt` та `pyproject.toml`, замінюючи `zep-cloud` на `zep-python`.
2. Рекурсивно сканує директорію `backend/` і замінює імпорти `from zep_cloud` на `from zep_python`.
3. Замінює класи `ZepCloudClient` на `ZepClient`.

## 3. Базовий CI/CD (GitHub Actions)

Для забезпечення стабільності коду рекомендується використовувати наступний пайплайн `.github/workflows/ci.yml` (приклад):

```yaml
name: MiroFish CI

on:
  push:
    branches: [ "main" ]
  pull_request:
    branches: [ "main" ]

jobs:
  build:
    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@v3
    
    - name: Setup Node.js
      uses: actions/setup-node@v3
      with:
        node-version: '18'
        
    - name: Setup Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'
        
    - name: Install uv
      run: curl -LsSf https://astral.sh/uv/install.sh | sh
      
    - name: Install Dependencies
      run: npm run setup:all
      
    - name: Run Linter (Frontend)
      run: cd frontend && npm run lint
```

## 4. Zero-config підхід

Проект спроектовано таким чином, щоб мінімізувати ручні налаштування:
- Використання `uv` дозволяє уникнути проблем із конфліктами версій Python-пакетів.
- Docker Compose автоматично зв'язує порти між контейнерами.
- Динамічне завантаження мов (i18n) на фронтенді працює без потреби перебудови (rebuild) при додаванні нових `json` файлів у теку `locales/`.

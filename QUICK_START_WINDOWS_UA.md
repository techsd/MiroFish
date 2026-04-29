# 🚀 MiroFish - Швидкий Старт (Windows 11 + PowerShell 7)

> **За 5 хвилин від нуля до запуску на Windows 11 з PowerShell 7**

---

## 📋 Що таке MiroFish?

**MiroFish** — мульти-агентний AI движок для прогнозування на основі групової інтелектуальності.

- **Backend:** Python 3.11-3.12 + Flask
- **Frontend:** Vue 3 + Vite
- **Особливість:** Zero-config автоматизація

---

## ⚡ Швидкий Старт (5 хвилин)

### **1. Встановіть Prerequisites**

Відкрийте **PowerShell 7 як Administrator** та виконайте:

```powershell
winget install OpenJS.NodeJS Python.Python.3.12
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

**Перевірка:**
```powershell
node -v
python --version
uv --version
```

---

### **2. Клонування + Конфігурація**

```powershell
git clone https://github.com/techsd/MiroFish.git
cd MiroFish
Copy-Item .env.example .env
notepad .env
```

**Заповніть в `.env`:**
```env
LLM_API_KEY=your_api_key_here
LLM_BASE_URL=https://dashscope.aliyuncs.com/compatible-mode/v1
LLM_MODEL_NAME=qwen-plus

ZEP_API_KEY=your_zep_api_key_here
```

> 💡 Ключі отримайте на: [Alibaba Bailian](https://bailian.console.aliyun.com/) + [Zep Cloud](https://app.getzep.com/)

---

### **3. Автоматична Установа**

```powershell
npm run setup:all
```

**Що відбувається:**
- ✅ Node deps (root + frontend)
- ✅ Python venv + deps (backend)
- ✅ Автоматична конфігурація

> ⏱️ ~3-5 хвилин

---

### **4. Запуск**

```powershell
npm run dev
```

**Готово! 🎉**
- 🌐 Frontend: http://localhost:3000
- ⚙️ Backend: http://localhost:5001

---

## 🛠️ Окремий Запуск

```powershell
npm run backend    # Тільки backend
npm run frontend   # Тільки frontend
npm run build      # Production build
```

---

## 🐳 Docker (без Python)

```powershell
winget install Docker.DockerDesktop

cp .env.example .env
# Редагуйте .env

docker compose up -d
# http://localhost:3000 + http://localhost:5001
```

---

## ❌ Проблеми & Рішення

| Проблема | Рішення |
|----------|---------|
| `uv` не знайдено | Перезавантажте PowerShell |
| Port 3000/5001 зайнятий | `taskkill /FI "MEMUSAGE gt 0"` або `netstat -ano \| findstr :3000` |
| Python не знайдено | Переустановіть Python або оновіть PATH |
| npm ERR! | `rm -r node_modules`, `npm cache clean --force`, `npm install` |
| venv issues | `rm -r backend\.venv`, `uv sync` |

---

## 📂 Структура Проекту

```
MiroFish/
├── backend/           # Flask API (Python 3.12)
│   ├── app/
│   ├── pyproject.toml
│   └── run.py
├── frontend/          # Vue 3 + Vite
│   ├── src/
│   └── package.json
├── .env               # Config (from .env.example)
├── package.json       # Root scripts
└── docker-compose.yml
```

---

## 📝 Команди (Шпаргалка)

```powershell
# Install all dependencies
npm run setup:all

# Start frontend + backend
npm run dev

# Backend only
npm run backend

# Frontend only
npm run frontend

# Production build
npm run build

# Docker
docker compose up -d
docker compose down
```

---

## 🔗 Посилання

- 📖 [GitHub](https://github.com/techsd/MiroFish)
- 🌐 [Live Demo](https://mirofish.ai)
- 💬 [Discord](http://discord.gg/ePf5aPaHnA)
- 🐦 [X/Twitter](https://x.com/mirofish_ai)
- 📷 [Instagram](https://www.instagram.com/mirofish_ai/)

---

## ✨ Готово!

1. ✅ Встановлено Prerequisites
2. ✅ Налаштовано `.env`
3. ✅ Запущено `npm run setup:all`
4. ✅ Стартовано `npm run dev`
5. ✅ Відкрито http://localhost:3000

**Ви готові до мульти-агентного прогнозування! 🎯**

---

## 💬 Історія чату

### Запит користувача:
> Збережі цей чат в один файл markdown

### Контекст:
- Попередній чат містив детальний гайд по автоматизації zero config для розгортання MiroFish
- Користувач запросив спрощену версію
- Усі команди оптимізовані для Windows 11 + PowerShell 7
- Гайд охоплює: встановлення, конфігурацію, запуск, troubleshooting та Docker альтернативу

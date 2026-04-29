# 🚀 **MiroFish - Zero Config Guide для Windows 11 UA + PowerShell 7**

## **Про проект**
**MiroFish** — мульти-агентний AI движок для прогнозування на основі групової інтелектуальності. Стек: Python 3.11-3.12 (backend) + Node.js 18+ (frontend).

---

## **📋 ПІДГОТОВКА (One-Click)**

### **1️⃣ Встановіть Prerequisites**

**Відкрийте PowerShell 7 як Administrator** та виконайте:

```powershell
# Установа Node.js 20 LTS
winget install OpenJS.NodeJS

# Установа Python 3.12
winget install Python.Python.3.12

# Установа uv (Python package manager)
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# Перевірка
node -v
python --version
uv --version
```

---

## **🔑 КОНФІГУРАЦІЯ (Zero Config Magic)**

### **2️⃣ Клонування + .env Setup**

```powershell
# Клон репозиторія
git clone https://github.com/techsd/MiroFish.git
cd MiroFish

# Копіювання конфіг файла
Copy-Item .env.example .env

# Редагування (відкриється Notepad)
notepad .env
```

**Заповніть обов'язкові параметри:**
```env
LLM_API_KEY=your_key_here
LLM_BASE_URL=https://dashscope.aliyuncs.com/compatible-mode/v1
LLM_MODEL_NAME=qwen-plus

ZEP_API_KEY=your_zep_key_here
```

> 💡 **Без цих ключів = demo-режим (обмежено)**

---

## **⚡ АВТОМАТИЧНА УСТАНОВА (One Command)**

### **3️⃣ Full Setup**

```powershell
# ВЕСЬ СТЕК в одну команду
npm run setup:all
```

**Що відбувається за кулісами:**
- ✅ Node deps (root + frontend)
- ✅ Python venv + deps (backend)
- ✅ Автоматична конфігурація

> ⏱️ Займає ~3-5 хвилин

---

## **🎯 ЗАПУСК**

### **4️⃣ Start Services**

```powershell
# ДВА сервіси паралельно (frontend + backend)
npm run dev
```

**Готово! Отримаєте:**
- 🌐 Frontend: `http://localhost:3000`
- ⚙️ Backend API: `http://localhost:5001`

**Або окремо:**
```powershell
npm run backend    # Тільки backend
npm run frontend   # Тільки frontend
```

---

## **🛠️ УПРАВЛІННЯ (Advanced)**

### **Backend Only (PowerShell)**

```powershell
cd backend
uv run python run.py
```

### **Frontend Only**

```powershell
cd frontend
npm run dev
```

### **Production Build**

```powershell
npm run build
# Output: ./frontend/dist/
```

---

## **🐳 Docker (Альтернатива)**

Якщо НЕ хочете встановлювати Python:

```powershell
# 1. Встановіть Docker Desktop для Windows
winget install Docker.DockerDesktop

# 2. Setup
cp .env.example .env
# Відредагуйте .env (notepad .env)

# 3. Run
docker compose up -d

# 4. URLs: http://localhost:3000 + http://localhost:5001
```

---

## **❌ Troubleshooting**

| Проблема | Рішення |
|----------|---------|
| **`uv` не знайдено** | Перезавантажте PowerShell, оновіть PATH |
| **Port 3000/5001 зайнятий** | `netstat -ano \| findstr :3000` → `taskkill /PID <id>` |
| **Python не знайдено** | Перевірте PATH або переустановіть Python |
| **npm ERR!** | Видаліть `node_modules/`, виконайте `npm cache clean --force`, потім `npm install` |
| **venv issues** | Удаліть `backend/.venv`, виконайте `uv sync` заново |

---

## **📊 Project Structure**

```
MiroFish/
├── backend/                # Flask API (Python 3.12)
│   ├── app/               # Main application
│   ├── pyproject.toml     # Dependencies
│   └── run.py             # Entry point
├── frontend/              # Vue 3 + Vite
│   ├── src/
│   └── package.json
├── .env                   # Config (create from .env.example)
├── package.json           # Root scripts
└── docker-compose.yml     # Docker setup
```

---

## **🚀 Quick Commands Cheatsheet**

```powershell
# Install ALL
npm run setup:all

# Start ALL
npm run dev

# Backend only
npm run backend

# Frontend only
npm run frontend

# Build frontend
npm run build

# Docker
docker compose up -d
docker compose down
```

---

## **✨ Готово!**

1. ✅ Встановлено Prerequisites
2. ✅ Налаштовано .env
3. ✅ Запущено `npm run setup:all`
4. ✅ Стартовано `npm run dev`
5. ✅ Відкрито http://localhost:3000

**Ви готові до мульти-агентного прогнозування!** 🎯

---

**Питання?** Дивіться [офіційну документацію](https://github.com/666ghj/MiroFish) або Discord: http://discord.gg/ePf5aPaHnA

# Ayanm – Vedic Time Companion (Ayan OS)

The world's best Vedic Time operating system. Stay connected with Vedic time — beautiful, minimal, and premium.

## 🌟 Features

- **Live Vedic Clock** — Real-time Muhurta, Tithi, Nakshatra, Yoga, Karana
- **Today's Panchanga** — Sunrise, Sunset, Brahma Muhurta, Rahu Kaal, and more
- **Daily Guidance** — Contextual spiritual explanations based on current Nakshatra
- **Festival Engine** — Countdowns and significance of Indian festivals worldwide
- **Home Widgets** — Small, Medium, Large widgets for quick glances
- **Global Geolocation** — Accurate calculations based on your exact location
- **Offline Mode** — 1 year of Panchanga stored locally
- **Cross-Platform** — Android, iOS, Web from a single codebase

## 🏗️ Architecture

```
arian/
├── backend/          # FastAPI + Python
├── frontend/         # Flutter (Android/iOS/Web)
├── database/         # PostgreSQL init & migrations
└── docker-compose.yml
```

## 🚀 Quick Start

### Prerequisites
- Docker & Docker Compose
- Python 3.11+
- Flutter SDK 3.x (for frontend development)

### Backend Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate   # or venv\Scripts\activate on Windows
pip install -r requirements.txt
cp .env.example .env       # Edit with your credentials
alembic upgrade head
uvicorn app.main:app --reload
```

### Frontend Setup

```bash
cd frontend
flutter pub get
flutter run
```

### Docker Compose (All Services)

```bash
docker-compose up -d
```

Services: PostgreSQL, Redis, Backend API, Flutter Web

## 📚 API Documentation

Once the backend is running, visit:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## 🧪 Testing

```bash
# Backend
cd backend
pytest -v

# Frontend
cd frontend
flutter test
```

## 📖 Tech Stack

| Layer       | Technology        |
|-------------|-------------------|
| Frontend    | Flutter           |
| Backend     | Python FastAPI    |
| Database    | PostgreSQL        |
| Cache       | Redis             |
| Auth        | JWT (python-jose) |
| Migrations  | Alembic           |
| Deploy      | Docker, Cloudflare|

## 📄 License

Proprietary — All Rights Reserved

### Running locally

1. **Backend**

   ```bash
   cd backend
   pip install -r requirements.txt
   python -m venv venv
   .\venv\Scripts\activate   # Windows
   uvicorn app.main:app --reload
   ```

2. **Frontend**

   ```bash
   cd frontend
   flutter pub get
   flutter run
   ```

The app will call the backend at `http://localhost:8000/vedic-time`.

You can also spin up everything with Docker Compose:

```bash
docker compose up --build
```

Backend will be available on `http://localhost:8000` and the Redis cache on `6379`.

# ghadi

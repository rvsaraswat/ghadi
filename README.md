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

## Cosmic Panchanga

The browser dashboard includes a Cosmos view at **Cosmos** in the main navigation. It exposes the sidereal inputs behind Tithi, Nakshatra, Yoga, and Karana; an SVG zodiac and 27-segment Nakshatra ring; planet telemetry; playback from -7 to +30 days; transition cards; and an educational solar-system orbit model.

The API contract is `GET /panchanga/cosmic?at=YYYY-MM-DDTHH:MM:SS&ayanamsha=27`. The calculation service returns Lahiri metadata and keeps the ephemeris provider behind `get_cosmic_panchanga()`, so a `pysweph` implementation can replace the current educational mean-orbit provider without changing the dashboard contract. The current repository does not yet vendor Swiss Ephemeris or a React/TypeScript build, so the shipped implementation intentionally remains compatible with the existing FastAPI static dashboard and labels the provider boundary in code.

Run the browser dashboard locally with `cd backend` followed by `python -m uvicorn app.main:app --reload`, then open `http://localhost:8000`.

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

For a home-server deployment, create a root `.env` file before building and
replace the example address with the server's LAN address:

```dotenv
API_BASE_URL=http://192.168.1.100:28000
FRONTEND_PORT=3001
```

The frontend embeds this value during its Docker build. `localhost` would point
to the device running the browser, not the home server. Open the UI at
`http://192.168.1.100:3001` unless you choose another `FRONTEND_PORT`.

Backend will be available on `http://localhost:8000` and the Redis cache on `6379`.

# ghadi

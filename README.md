# ✈️ SkyRoute — Flight Booking & Recommendation System

SkyRoute is a full-stack flight booking platform that combines a complete booking workflow with real-time seat locking, dynamic pricing, and personalized flight recommendations.

## 🚀 Live Demo

**Frontend:** https://skyroute-flight-booking-system.vercel.app

**Backend API / Swagger:** https://flight-booking-system-kqtg.onrender.com/docs

---

## ✨ Features

### 👤 Authentication
- User registration and login
- JWT-based authentication
- Role-based authorization
- Protected user and admin endpoints

### 🔎 Flight Search
- Search flights by origin, destination, and departure date
- Airport autocomplete/search
- Direct flight results
- Alternative one-stop routes

### 🤖 Flight Recommendations
Three recommendation modes:

- **Cheapest** — prioritizes lower fares
- **Fastest** — prioritizes shorter duration
- **Balanced** — balances price, duration, and stops

The recommendation engine normalizes individual factors into comparable 0–1 scores before calculating the final weighted score.

### 💺 Seat Selection
- Visual airplane seat map
- Business and Economy sections
- Window, middle, and aisle positions
- Seat availability tracking
- Client-side seat selection

### 🔒 Concurrent Seat Locking
Redis is used to temporarily lock seats during checkout.

- Lock duration: **300 seconds**
- Prevents two users from booking the same seat concurrently
- Handles seat conflicts gracefully
- Unpaid bookings are automatically expired

### 💰 Dynamic Pricing
The system dynamically adjusts flight prices based on:

- Seat occupancy
- Time remaining before departure

Pricing adjustments are capped to prevent unrealistic fare changes.

### 💳 Payment Workflow
- Multiple payment methods
- Payment success/failure simulation
- Retry handling
- Booking state transitions
- Automatic handling of expired seat holds

### 📋 Booking Management
- PNR generation
- Booking summary
- Seat and passenger information
- Payment status
- My Bookings page

---

## 🏗️ System Architecture

```text
                         ┌──────────────────────┐
                         │      React/Vite      │
                         │      Frontend        │
                         └──────────┬───────────┘
                                    │
                              REST API / JWT
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │       FastAPI        │
                         │       Backend        │
                         └──────┬───────┬───────┘
                                │       │
                    ┌───────────┘       └────────────┐
                    ▼                                ▼
             ┌──────────────┐                 ┌──────────────┐
             │ PostgreSQL   │                 │    Redis     │
             │              │                 │              │
             │ Users        │                 │ Seat locks   │
             │ Flights      │                 │ TTL: 300 sec │
             │ Seats        │                 │              │
             │ Bookings     │                 └──────────────┘
             │ Payments     │
             └──────────────┘
```

## 🧠 Key Engineering Decisions

### 🔒 Redis-Based Seat Locking

To prevent concurrent users from booking the same seat, SkyRoute uses Redis-based temporary seat locks.

When a user confirms a seat:

1. The backend checks the seat's availability.
2. A Redis lock is acquired for the selected seat.
3. The booking is created while the seat is held.
4. The lock remains valid for 300 seconds.
5. If payment is not completed within the hold period, the booking is automatically expired and the seat becomes available again.

This prevents double-booking when multiple users attempt to reserve the same seat concurrently.

### 💰 Dynamic Pricing

SkyRoute includes a dynamic pricing engine that adjusts flight fares based on:

- Seat occupancy
- Time remaining before departure

Individual pricing adjustments are capped at 15%, while the cumulative adjustment is capped at 50% to prevent unrealistic price fluctuations.

```text
Base Price
    │
    ├── Occupancy Adjustment
    │
    └── Time-Based Adjustment
             │
             ▼
       Current Price
```

## 📁 Project Structure

```text
Flight-Booking-System/
│
├── backend/
│   ├── alembic/              # Database migrations
│   │
│   ├── app/
│   │   ├── api/              # API route handlers
│   │   ├── core/             # Configuration and database setup
│   │   ├── dependencies/     # FastAPI dependencies
│   │   ├── jobs/             # Scheduled background jobs
│   │   ├── layout/           # Seat layout configuration
│   │   ├── models/           # SQLAlchemy database models
│   │   ├── repositories/     # Database access layer
│   │   ├── schemas/          # Pydantic schemas
│   │   ├── services/         # Business logic
│   │   ├── user/             # User-related functionality
│   │   ├── utils/            # Utility functions
│   │   └── main.py           # FastAPI application entry point
│   │
│   ├── scripts/              # Database seeding scripts
│   ├── alembic.ini           # Alembic configuration
│   └── requirements.txt      # Backend dependencies
│
frontend/React/
│
├── public/                   # Static assets
│
├── src/
│   ├── admin/                # Admin-related components/pages
│   ├── api/                  # API request functions
│   ├── components/          # Reusable React components
│   ├── context/             # React context providers
│   ├── CSS/                 # Component/page styles
│   ├── hooks/                # Custom React hooks
│   ├── pages/
│   │   ├── auth/             # Login and registration
│   │   └── user/             # User-facing application pages
│   ├── routes/               # React Router configuration
│   ├── utils/                # Utility functions
│   ├── App.jsx               # Root application component
│   ├── index.css             # Global styles
│   └── main.jsx              # Application entry point
│
├── package.json
├── vite.config.js
└── index.html
│
└── README.md
```

## ⚙️ Local Setup

### Prerequisites

Make sure you have the following installed:

- Python 3.10+
- Node.js 18+
- PostgreSQL
- Redis
- Git

### 1. Clone the Repository

```bash
git clone https://github.com/roshanmishra17/Flight-Booking-System.git
cd Flight-Booking-System

python -m venv venv

.\venv\Scripts\activate

pip install -r requirements.txt

uvicorn main:app --reload
```

## API Documentation

Swagger UI is available at:

http://localhost:8000/docs

## Environment Variables

Create a `.env` file in the project root with the following values:

```env
DATABASE_URL=postgresql://user:password@host:port/db
SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_TIME=60
```

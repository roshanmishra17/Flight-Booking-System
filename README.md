# ✈️ SkyRoute — Intelligent Flight Recommendation & Booking Platform

SkyRoute is a full-stack domestic flight booking system built to demonstrate backend engineering depth through concurrent seat locking, dynamic pricing, a weighted recommendation engine, alternative route discovery, and a retry-safe payment workflow.

**Live Demo:** https://skyroute-flight-booking-system.vercel.app

**API:** https://flight-booking-system-kqtg.onrender.com

**Swagger Documentation:** https://flight-booking-system-kqtg.onrender.com/docs

**GitHub:** https://github.com/roshanmishra17/Flight-Booking-System

---

## Why This Project Is Different

Most student booking projects follow:

```text
Search → Book
```

SkyRoute implements a more complete booking workflow:

```text
Search
   ↓
Recommendation Engine
   ↓
Explainable Ranking
   ↓
Seat Selection
   ↓
Redis Seat Lock
   ↓
Booking
   ↓
Concurrency-Safe Confirmation
   ↓
Dynamic Pricing
   ↓
Payment
   ↓
Retry-Safe Failure Handling
   ↓
Cancellation & Refund
```

The project focuses on backend concepts such as concurrency control, data consistency, transaction boundaries, dynamic pricing, recommendation scoring, and failure handling rather than only basic CRUD operations.

---

## ✨ Core Features

### 👤 Authentication & Authorization

- User registration and login
- JWT-based authentication
- Protected routes
- Role-based authorization
- User and admin access control

### 🔎 Flight Search

- Search flights by origin, destination, departure date, and travel class
- Airport search and selection
- Direct flight search
- Flight details including airline, duration, price, aircraft type, and stops

### 🤖 Flight Recommendation Engine

SkyRoute supports three recommendation modes:

- **Cheapest** — prioritizes lower fares
- **Fastest** — prioritizes shorter flight duration
- **Balanced** — balances price, duration, and stops

The recommendation engine normalizes price, duration, and stop count into comparable 0–1 scores before applying mode-specific weights.

### 🔀 Alternative Route Discovery

- Automatically discovers one-stop alternative routes
- Minimum layover: **45 minutes**
- Maximum layover: **4 hours**
- Returns the top **3 ranked alternatives**
- Calculates total duration and estimated price

### 💺 Seat Selection

- Visual airplane seat map
- Business and Economy class sections
- Window, middle, and aisle seat positions
- Seat availability tracking
- Seat-specific price multipliers
- Client-side seat selection before booking confirmation

### 🔒 Redis-Based Seat Locking

Redis is used for temporary seat locking during booking creation.

- Atomic Redis `SET NX EX` locking
- Lock duration: **300 seconds**
- Prevents concurrent double-booking
- Automatically expires abandoned seat holds
- Handles seat conflicts gracefully

### 💰 Dynamic Pricing

Flight prices are dynamically calculated using:

- Seat occupancy
- Time remaining before departure

The pricing engine applies bounded adjustments to prevent unrealistic fare fluctuations.

- Individual adjustment cap: **15%**
- Cumulative adjustment cap: **50%**

The stored `base_price` remains unchanged while the current fare is calculated dynamically.

### 💳 Payment Workflow

- Mock payment system
- UPI, credit card, and debit card options
- Simulated payment success/failure
- Retry-safe payment handling
- Prevents duplicate payment records on retry
- Booking status transitions
- Automatic handling of expired seat holds

### 📋 Booking Management

- PNR generation
- Booking summary
- Passenger information
- Seat information
- Booking status
- Payment status
- Booking cancellation
- Automatic refund logic
- Seat release after cancellation
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
             │ Airports     │                 │ TTL: 300 sec │
             │ Flights      │                 │              │
             │ Seats        │                 └──────────────┘
             │ Bookings     │
             │ Payments     │
             └──────────────┘
```

---

## 🧠 Key Engineering Decisions

### 🔒 Concurrency-Safe Seat Locking

Seat availability is protected at multiple levels.

When a user confirms a seat:

```text
User selects seat
       ↓
POST /bookings
       ↓
Check seat availability
       ↓
Acquire Redis lock using SET NX EX
       ↓
Create booking
       ↓
Seat remains temporarily locked
       ↓
Payment
```

The Redis lock prevents concurrent requests from acquiring the same seat during the booking process.

A database-level constraint provides an additional integrity backstop against multiple confirmed bookings for the same seat.

Unpaid bookings are automatically expired after the hold period, releasing the seat for future users.

### 💰 Dynamic Pricing Without Mutating Stored Data

The stored `base_price` remains unchanged after a flight is created.

The current fare is calculated from:

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

The booking stores the final `total_price` at booking time.

This means historical bookings retain the exact price that was charged, even if the flight's dynamic price changes later.

### 🤖 Weighted Recommendation Engine

Flight attributes are normalized before calculating recommendation scores:

```text
Price ────────┐
Duration ─────┼──> Normalize → Apply Weights → Final Score → Ranking
Stops ────────┘
```

Different weights are applied for:

- Cheapest
- Fastest
- Balanced

This allows the same flight dataset to be ranked according to different user preferences.

### 🔀 Alternative Route Discovery

The alternative-route engine combines compatible flight legs to discover one-stop journeys.

The system validates:

```text
Minimum layover: 45 minutes
Maximum layover: 4 hours
Maximum alternatives returned: 3
```

Each candidate route is evaluated using its combined duration and estimated price before ranking.

### 🗄️ Layered Backend Architecture

The backend follows a layered architecture:

```text
Models
   ↓
Schemas
   ↓
Repositories
   ↓
Services
   ↓
API Routers
```

- **Models** define database entities.
- **Schemas** define API request and response structures.
- **Repositories** handle database access.
- **Services** contain business logic and transaction boundaries.
- **API routers** handle HTTP requests and map domain errors to appropriate responses.

### 💺 Derived Seat Availability

Seat availability is not stored as a separate `is_available` field.

Instead, availability is determined from the current booking state and active Redis lock.

This avoids maintaining multiple independent sources of truth for seat availability.

### 👨‍💼 Admin Scope

The backend implements admin capabilities including:

- Flight CRUD
- Airport CRUD
- Automatic seat generation
- Role-protected admin operations

A full admin frontend is intentionally scoped out. The primary focus of the project is the customer booking workflow and the backend engineering challenges around concurrency, pricing, recommendations, and payment state management.

### 🌍 Domestic-Only Design

The system is designed for domestic flight bookings and uses a single timezone model for the current implementation.

---

## 🛠️ Tech Stack

### Frontend

- React
- Vite
- React Router
- Axios
- React Hook Form
- CSS

### Backend

- Python
- FastAPI
- SQLAlchemy
- Pydantic
- JWT Authentication
- REST APIs
- APScheduler
- Alembic

### Database & Infrastructure

- PostgreSQL
- Redis
- Supabase
- Render
- Vercel

---

## 📁 Project Structure

```text
Flight-Booking-System/
│
├── backend/
│   ├── alembic/                  # Database migrations
│   │
│   ├── app/
│   │   ├── api/                  # FastAPI API routes
│   │   ├── core/                 # Configuration and database setup
│   │   ├── dependencies/         # FastAPI dependencies
│   │   ├── jobs/                 # Scheduled background jobs
│   │   ├── layout/               # Aircraft seat layout configuration
│   │   ├── models/               # SQLAlchemy database models
│   │   ├── repositories/         # Database access layer
│   │   ├── schemas/              # Pydantic schemas
│   │   ├── services/             # Business logic
│   │   ├── user/                 # User-related functionality
│   │   ├── utils/                # Utility functions
│   │   └── main.py               # FastAPI application entry point
│   │
│   ├── scripts/                  # Database seeding scripts
│   ├── alembic.ini               # Alembic configuration
│   └── requirements.txt          # Backend dependencies
│
├── frontend/
│   └── React/
│       ├── public/               # Static assets
│       │
│       ├── src/
│       │   ├── admin/            # Admin functionality
│       │   ├── api/              # API request functions
│       │   ├── components/       # Reusable React components
│       │   ├── context/           # React context providers
│       │   ├── CSS/               # Stylesheets
│       │   ├── hooks/             # Custom React hooks
│       │   ├── pages/
│       │   │   ├── auth/           # Authentication pages
│       │   │   └── user/           # User-facing pages
│       │   ├── routes/             # React Router configuration
│       │   ├── utils/              # Utility functions
│       │   ├── App.jsx             # Root application component
│       │   ├── index.css           # Global styles
│       │   └── main.jsx            # Application entry point
│       │
│       ├── package.json
│       ├── vite.config.js
│       └── index.html
│
└── README.md
```

---

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
```

### 2. Backend Setup

```bash
cd backend

python -m venv venv
```

Activate the virtual environment.

**Windows:**

```bash
.\venv\Scripts\activate
```

**macOS/Linux:**

```bash
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

### 3. Environment Variables

Create a `.env` file inside the `backend` directory:

```env
DATABASE_URL=postgresql://user:password@host:port/db
SECRET_KEY=your_secret_key
REDIS_URL=your_redis_url
ALGORITHM=HS256
ACCESS_TOKEN_TIME=60
```

Do not commit the actual `.env` file or secret values to GitHub.

### 4. Run Database Migrations

From the `backend` directory:

```bash
alembic upgrade head
```

### 5. Seed Development Data

To populate the development database with airports, flights, and seats:

```bash
python scripts/seed.py
```

### 6. Start the Backend

```bash
uvicorn app.main:app --reload
```

The backend will run at:

```text
http://localhost:8000
```

### 7. Frontend Setup

Open a new terminal:

```bash
cd frontend/React
```

Install dependencies:

```bash
npm install
```

Create a `.env` file inside the `frontend/React` directory:

```env
VITE_API_URL=http://localhost:8000
```

Start the development server:

```bash
npm run dev
```

The frontend will be available at:

```text
http://localhost:5173
```

### 8. Production Build

Create a production build:

```bash
npm run build
```

Preview the production build locally:

```bash
npm run preview
```

---

## 📚 API Documentation

SkyRoute uses FastAPI's built-in Swagger UI for interactive API documentation.

### Local Swagger

After starting the backend:

```text
http://localhost:8000/docs
```

### Live Swagger

https://flight-booking-system-kqtg.onrender.com/docs

The API includes endpoints for:

- Authentication
- Airports
- Flight search
- Flight recommendations
- Alternative routes
- Seat maps
- Bookings
- Payments
- User bookings
- Admin operations

---

## 📋 API Overview

| Resource | Endpoints |
|---|---|
| Auth | `POST /auth/register`, `POST /auth/login` |
| Users | `GET /user/me` |
| Airports | `GET /airports`, admin CRUD |
| Flights | `GET /flights/search`, `GET /flights/search/ranked`, `GET /flights/search/alternatives`, admin CRUD |
| Seats | `GET /flights/{id}/seats` |
| Bookings | `POST /bookings`, `GET /bookings/me`, `GET /bookings/{id}`, `PATCH /bookings/{id}/cancel` |
| Payments | `POST /payments`, `GET /payments/{id}` |

For the complete API specification, use the interactive Swagger documentation.

---

## 🚀 Deployment

### Frontend

The React frontend is deployed on Vercel.

**Live Application:**

https://skyroute-flight-booking-system.vercel.app

### Backend

The FastAPI backend is deployed on Render.

**Live API:**

https://flight-booking-system-kqtg.onrender.com

**Swagger Documentation:**

https://flight-booking-system-kqtg.onrender.com/docs

### Database

PostgreSQL is hosted using Supabase.

### Redis

Redis is used for temporary seat locking during the booking workflow.

---

## 📸 Screenshots

### Home & Flight Search

<img width="2614" height="1516" alt="image" src="https://github.com/user-attachments/assets/192f88b7-8001-4a9c-8c21-93a023ac6397" />

### Flight Search Results

<img width="2476" height="1494" alt="image" src="https://github.com/user-attachments/assets/4029be95-751f-4ee8-a694-f9d9c5c6670e" />

### Seat Selection

<img width="2400" height="1470" alt="image" src="https://github.com/user-attachments/assets/073bd6f7-ec9e-4f4a-b275-6157054cb44d" />

### Booking Summary
<img width="2304" height="1502" alt="image" src="https://github.com/user-attachments/assets/be0a5fd8-5732-493b-b672-3d1bbc32a73d" />

### Payment

<img width="2324" height="1334" alt="image" src="https://github.com/user-attachments/assets/abdd9754-0bb4-4ce2-ac54-bce7383df7a7" />


### My Bookings

<img width="2440" height="1504" alt="image" src="https://github.com/user-attachments/assets/1bbdffde-defa-4057-b796-72973164f712" />

---

## 🔮 Future Improvements

- Redis-based caching for frequently repeated flight searches
- Search history
- Full admin dashboard UI
- Integration with a real payment gateway
- Expanded flight and airport datasets

---

## 👨‍💻 Author

**Roshan Mishra**

B.Sc. Computer Science

GitHub: https://github.com/roshanmishra17

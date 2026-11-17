# Real-Time Network Attack Detection and Monitoring System (NIDS)

A full-stack, machine learning-powered Network Intrusion Detection System built with **Scapy**, **XGBoost**, **FastAPI**, **PostgreSQL**, and **React**.

---

## 📌 Project Overview

This project implements an end-to-end intrusion detection solution designed to:
1. **Sniff Network Packets:** Capture raw packets in real time and aggregate them into bi-directional flow records using **Scapy**.
2. **Machine Learning Inference:** Classify flow patterns into benign traffic or security threats (e.g., DoS/DDoS, Port Scanning, Brute Force) using an optimized **XGBoost** model.
3. **Real-Time Alert Dispatch:** Broadcast threats and network metadata via **FastAPI** WebSockets and persist alerts into a **PostgreSQL** database.
4. **Interactive Dashboard:** Provide a **React** web dashboard with live threat feeds, interactive traffic volume charts, and JWT-authenticated access.

---

## 🏗️ System Architecture

```
[ Network Traffic ]
        │ (Raw Packets)
        ▼
[ Scapy Sniffer & Flow Aggregator ]
        │ (Extracted Features)
        ▼
[ XGBoost ML Engine ] ──► [ Predictions & Severity ]
                                  │
                                  ▼
                    [ FastAPI Backend & WebSockets ]
                         ├── PostgreSQL (Persistent Storage)
                         └── React Web Dashboard (Live Stream)
```

---

## 📁 Repository Structure

```
network-ids/
├── ml_engine/             # XGBoost model training, preprocessing & evaluation
│   ├── data/              # Datasets (e.g. CIC-IDS2017)
│   ├── models/            # Saved model artifacts (.joblib, .json)
│   ├── notebooks/         # Jupyter notebooks for EDA and evaluation
│   └── src/               # Python ML scripts (train.py, evaluate.py, predictor.py)
│
├── backend/               # FastAPI REST API & WebSocket server
│   ├── app/
│   │   ├── api/v1/        # Authentication, alerts, and live WebSocket routes
│   │   ├── core/          # JWT auth, config, and PostgreSQL async engine
│   │   ├── models/        # SQLAlchemy database models
│   │   ├── schemas/       # Pydantic data schemas
│   │   └── services/      # Scapy sniffer & feature extraction pipeline
│   └── requirements.txt   # Python backend dependencies
│
├── frontend/              # React (Vite + Tailwind CSS) Dashboard
│   ├── src/
│   │   ├── components/    # Reusable UI components (LiveChart, AlertsTable)
│   │   ├── pages/         # Dashboard, AlertsHistory, Login, Settings
│   │   └── services/      # API & WebSocket connectors
│   └── package.json
│
├── docs/                  # Academic documentation & thesis chapters
└── docker-compose.yml     # Complete stack orchestration (PostgreSQL + FastAPI + React)
```

---

## 🚀 Getting Started

### Option 1: Run with Docker Compose (Recommended)
```bash
docker-compose up --build
```
- **Frontend Dashboard:** http://localhost:3000
- **FastAPI API & Docs:** http://localhost:8000/docs
- **PostgreSQL Database:** localhost:5432

---

### Option 2: Run Locally for Development

#### 1. Machine Learning Module
```bash
cd ml_engine
pip install -r requirements.txt
# Train model on your dataset
python -m src.train data/your_dataset.csv
```

#### 2. FastAPI Backend
```bash
cd backend
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

#### 3. React Frontend
```bash
cd frontend
npm install
npm run dev
```

---

## 👥 Author & Git Details
- **Developer:** MUSTAPHA ALIYU UMAR
- **Email:** mustaphaaliyuumar825@gmail.com
- **Repository:** [Aliyu-Musty/network-ids](https://github.com/Aliyu-Musty/network-ids)

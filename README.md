# F1 Analytics Platform 🏎️

An end-to-end data platform for Formula 1 analytics — from raw telemetry ingestion to ML-powered race predictions and an interactive dashboard.

## Architecture
```
OpenF1 API + Ergast API
        ↓
  Prefect Pipeline (Python)
        ↓
S3 (raw) → PostgreSQL (warehouse)
        ↓
 pandas + dbt (transforms)
        ↓
  XGBoost ML Model
        ↓
  Node.js REST API
        ↓
  Next.js Dashboard
```

## Tech Stack

| Layer | Technology |
|---|---|
| Orchestration | Prefect |
| Ingestion | Python, requests, pandas |
| Storage | PostgreSQL, AWS S3 |
| Transformation | pandas, dbt |
| ML | scikit-learn, XGBoost |
| API | Node.js, Express |
| Frontend | Next.js, Recharts |
| Infrastructure | Docker, AWS ECS, AWS RDS |

## Project Structure
```
f1-analytics-platform/
├── pipeline/       # Python ETL pipeline (Prefect)
├── api/            # Node.js REST API
├── frontend/       # Next.js dashboard
├── infra/          # AWS infrastructure configs
└── docker-compose.yml
```

## Getting Started

### Prerequisites
- Docker 29+
- Node.js 24+
- Python 3.14+
- AWS CLI configured

### Running locally
```bash
# Copy environment variables
cp .env.example .env

# Start all services
docker-compose up --build
```

## Roadmap

- [x] Project setup & architecture
- [x] Data ingestion pipeline (OpenF1 + Ergast)
- [x] Data warehouse schema (PostgreSQL)
- [x] dbt transformations
- [ ] ML prediction model
- [ ] REST API
- [ ] Interactive dashboard
- [ ] AWS deployment

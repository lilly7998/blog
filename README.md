# Euro area dashboard

Small FastAPI app (ECB Data Portal + FRED public data) deployed on blitz.cloud at https://euro.andy.prod.page/.
Uses `DATABASE_URL` (PostgreSQL) as a 6-hour cache when present, otherwise memory. Listens on `$PORT`.
ECB meeting dates live in `meetings.json` (press-conference days, from the ECB calendar).

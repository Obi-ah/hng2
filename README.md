#  HNG2

A FastAPI service that fetches, enriches, and serves global country data (population, GDP, currency, flags) from external APIs, stores it in MySQL, and generates a visual summary.

##  Features
- Refresh country data from external APIs  
- Filter/sort by region or currency  
- Fetch or delete by name  
- Summary image of top 5 GDPs  
- Status endpoint with total and last refresh

## ️ Tech Stack
FastAPI · SQLAlchemy · MySQL · REST Countries API · Open Exchange Rate API

##  Endpoints
| Method | Endpoint | Description |
|--------|-----------|-------------|
| POST | `/countries/refresh` | Fetch and upsert countries |
| GET | `/countries` | List countries (filter/sort) |
| GET | `/countries/{name}` | Get details by name |
| DELETE | `/countries/{name}` | Delete a country |
| GET | `/countries/image` | Summary image |
| GET | `/status` | Service stats |

## 🧱 Setup
```bash
git clone <repo_url>
cd countries-api
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## 🧠 Example
**GET /status**
```json
{
  "total_countries": 249,
  "last_refreshed_at": "2025-10-28T14:00:00Z"
}


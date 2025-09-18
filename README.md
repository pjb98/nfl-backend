# NFL Backend API

Python Flask backend using nfl-data-py library to provide NFL schedule and stats data.

## Local Development

```bash
pip install -r requirements.txt
python main.py
```

Server runs on http://localhost:5001

## API Endpoints

- `GET /` - API info
- `GET /api/schedule/<season>/<week>` - Get NFL schedule for specific season/week
- `GET /api/standings/<season>` - Get standings for season
- `GET /api/team-stats/<season>` - Get team stats for season
- `GET /api/health` - Health check

## Deployment

This backend is designed to deploy on Railway, Heroku, or similar Python hosting platforms.

## Cache

All data is cached for 5 minutes to improve performance and reduce API calls.
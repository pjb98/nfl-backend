from flask import Flask, jsonify, request
from flask_cors import CORS
import nfl_data_py as nfl
import pandas as pd
from datetime import datetime
import os

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Cache to store data temporarily
cache = {}
CACHE_DURATION = 300  # 5 minutes in seconds

def is_cache_valid(cache_key):
    """Check if cached data is still valid"""
    if cache_key not in cache:
        return False

    cached_time = cache[cache_key]['timestamp']
    current_time = datetime.now().timestamp()
    return (current_time - cached_time) < CACHE_DURATION

def get_cached_or_fetch(cache_key, fetch_function, *args, **kwargs):
    """Get data from cache or fetch new data"""
    if is_cache_valid(cache_key):
        print(f"📦 Using cached data for {cache_key}")
        return cache[cache_key]['data']

    print(f"🔄 Fetching fresh data for {cache_key}")
    data = fetch_function(*args, **kwargs)

    # Store in cache
    cache[cache_key] = {
        'data': data,
        'timestamp': datetime.now().timestamp()
    }

    return data

@app.route('/')
def home():
    return jsonify({
        "message": "NFL Data API Backend",
        "status": "running",
        "endpoints": [
            "/api/schedule/<season>/<week>",
            "/api/standings/<season>",
            "/api/team-stats/<season>"
        ]
    })

@app.route('/api/schedule/<int:season>/<int:week>')
def get_schedule(season, week):
    """Get NFL schedule for a specific season and week"""
    try:
        cache_key = f"schedule_{season}_{week}"

        def fetch_schedule():
            # Get schedule data using nfl-data-py
            schedule_df = nfl.import_schedules([season])

            # Filter for specific week
            week_games = schedule_df[schedule_df['week'] == week]

            # Convert to JSON-serializable format
            games = []
            for _, game in week_games.iterrows():
                game_data = {
                    'game_id': str(game.get('game_id', '')),
                    'season': int(game.get('season', season)),
                    'week': int(game.get('week', week)),
                    'gameday': str(game.get('gameday', '')),
                    'weekday': str(game.get('weekday', '')),
                    'gametime': str(game.get('gametime', '')),
                    'away_team': str(game.get('away_team', '')),
                    'home_team': str(game.get('home_team', '')),
                    'away_score': int(game.get('away_score', 0)) if pd.notna(game.get('away_score')) else None,
                    'home_score': int(game.get('home_score', 0)) if pd.notna(game.get('home_score')) else None,
                    'result': int(game.get('result', 0)) if pd.notna(game.get('result')) else None,
                    'total': float(game.get('total', 0)) if pd.notna(game.get('total')) else None,
                    'overtime': int(game.get('overtime', 0)) if pd.notna(game.get('overtime')) else 0,
                    'old_game_id': str(game.get('old_game_id', '')),
                    'gsis_id': str(game.get('gsis_id', '')),
                    'nfl_detail_id': str(game.get('nfl_detail_id', '')),
                    'pfr': str(game.get('pfr', '')),
                    'pff': str(game.get('pff', '')),
                    'espn': str(game.get('espn', '')),
                    'ftn': str(game.get('ftn', '')),
                    'away_rest': int(game.get('away_rest', 0)) if pd.notna(game.get('away_rest')) else 0,
                    'home_rest': int(game.get('home_rest', 0)) if pd.notna(game.get('home_rest')) else 0,
                    'away_moneyline': float(game.get('away_moneyline', 0)) if pd.notna(game.get('away_moneyline')) else None,
                    'home_moneyline': float(game.get('home_moneyline', 0)) if pd.notna(game.get('home_moneyline')) else None,
                    'spread_line': float(game.get('spread_line', 0)) if pd.notna(game.get('spread_line')) else None,
                    'away_spread_odds': float(game.get('away_spread_odds', 0)) if pd.notna(game.get('away_spread_odds')) else None,
                    'home_spread_odds': float(game.get('home_spread_odds', 0)) if pd.notna(game.get('home_spread_odds')) else None,
                    'total_line': float(game.get('total_line', 0)) if pd.notna(game.get('total_line')) else None,
                    'under_odds': float(game.get('under_odds', 0)) if pd.notna(game.get('under_odds')) else None,
                    'over_odds': float(game.get('over_odds', 0)) if pd.notna(game.get('over_odds')) else None,
                    'div_game': int(game.get('div_game', 0)) if pd.notna(game.get('div_game')) else 0,
                    'roof': str(game.get('roof', '')),
                    'surface': str(game.get('surface', '')),
                    'temp': float(game.get('temp', 0)) if pd.notna(game.get('temp')) else None,
                    'wind': float(game.get('wind', 0)) if pd.notna(game.get('wind')) else None,
                    'away_qb_id': str(game.get('away_qb_id', '')),
                    'home_qb_id': str(game.get('home_qb_id', '')),
                    'away_qb_name': str(game.get('away_qb_name', '')),
                    'home_qb_name': str(game.get('home_qb_name', '')),
                    'away_coach': str(game.get('away_coach', '')),
                    'home_coach': str(game.get('home_coach', '')),
                    'referee': str(game.get('referee', '')),
                    'stadium_id': str(game.get('stadium_id', '')),
                    'stadium': str(game.get('stadium', ''))
                }
                games.append(game_data)

            return games

        games = get_cached_or_fetch(cache_key, fetch_schedule)

        return jsonify({
            'status': 'success',
            'data': games,
            'count': len(games),
            'season': season,
            'week': week
        })

    except Exception as e:
        print(f"❌ Error fetching schedule: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': str(e),
            'data': []
        }), 500

@app.route('/api/standings/<int:season>')
def get_standings(season):
    """Get NFL standings for a specific season"""
    try:
        cache_key = f"standings_{season}"

        def fetch_standings():
            # This would use nfl-data-py to get standings
            # For now, return a placeholder
            return []

        standings = get_cached_or_fetch(cache_key, fetch_standings)

        return jsonify({
            'status': 'success',
            'data': standings,
            'season': season
        })

    except Exception as e:
        print(f"❌ Error fetching standings: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': str(e),
            'data': []
        }), 500

@app.route('/api/team-stats/<int:season>')
def get_team_stats(season):
    """Get team stats for a specific season"""
    try:
        cache_key = f"team_stats_{season}"

        def fetch_team_stats():
            # This would use nfl-data-py to get team stats
            # For now, return a placeholder
            return {}

        stats = get_cached_or_fetch(cache_key, fetch_team_stats)

        return jsonify({
            'status': 'success',
            'data': stats,
            'season': season
        })

    except Exception as e:
        print(f"❌ Error fetching team stats: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': str(e),
            'data': {}
        }), 500

@app.route('/api/health')
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'cache_size': len(cache)
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5001))
    app.run(host='0.0.0.0', port=port, debug=False)
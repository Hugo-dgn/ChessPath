import requests
from datetime import datetime
from tqdm.auto import tqdm
import chess.pgn
import io

def fetch_chesscom_games(username, since_date, time_control):
    """
    Fetch Chess.com games for a user filtered by date and time control.

    Parameters:
    - username (str): Chess.com username.
    - since_date (str): Date in 'YYYY-MM-DD' format to filter games from.
    - time_control (str): Desired time control ('blitz', 'bullet', 'rapid', 'daily').

    Returns:
    - list: Filtered games matching the criteria.
    """
    # Convert since_date to a datetime object
    since_date = datetime.strptime(since_date, '%Y-%m-%d')
    year, month = since_date.year, since_date.month
    since_date_month = datetime(year, month, 1)

    # URL to fetch monthly archives
    headers = {'User-Agent': 'YourAppName/1.0 (your_email@example.com)'}
    url = f'https://api.chess.com/pub/player/{username}/games/archives'
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print("Failed to fetch archives:", response.status_code)
        return []
    archives = response.json()['archives']
    filtered_games = []

    for archive_url in tqdm(archives):
        # Extract year and month from the archive URL
        year, month = map(int, archive_url.split('/')[-2:])
        archive_date = datetime(year, month, 1)

        # Skip archives older than the specified date
        if archive_date < since_date_month:
            continue

        # Fetch games for this archive
        response = requests.get(archive_url, headers=headers)
        if response.status_code != 200:
            print(f"Failed to fetch games for {archive_url}")
            continue
        games = response.json()['games']
        # Filter games by time control
        for game in games:
            end_time = game["end_time"]
            date = datetime.fromtimestamp(end_time)
            if date < since_date:
                continue
            if game['time_control'] == time_control and game.get('rules', 'chess') == 'chess':
                game_pgn = chess.pgn.read_game(io.StringIO(game["pgn"]))
                if game_pgn:
                    filtered_games.append(game_pgn)
    return filtered_games

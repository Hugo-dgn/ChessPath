import requests

def get_most_common_moves(fen, rating_range, time_control, number_of_moves):
    # Base URL for Lichess opening explorer
    url = "https://explorer.lichess.ovh/lichess"
    
    # API parameters
    params = {
        "variant": "standard",
        "fen": fen,
        "ratings": ','.join(map(str, rating_range)),  # e.g., '1600,1800'
        "speeds": time_control,  # e.g., 'rapid'
        "moves": number_of_moves  # Number of moves to return (optional)
    }
    
    response = requests.get(url, params=params)
    data = response.json()
    
    moves = data["moves"]
    
    return moves

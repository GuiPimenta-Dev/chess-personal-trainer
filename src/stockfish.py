import requests


class Stockfish:
  
  def get_best_move(self, fen, depth):
    url = "https://chess-api.com/v1"
    payload = {"fen": fen, "depth": depth}
    response = requests.request("POST", url, json=payload)
    json_response = response.json()
    return json_response["move"]
 
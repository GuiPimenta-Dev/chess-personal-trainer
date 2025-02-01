import requests


class Stockfish:
  
  def get_best_move(self, fen):
    url = "https://chess-api.com/v1"
    payload = {"fen": fen}
    response = requests.request("POST", url, json=payload)
    json_response = response.json()
    return json_response["move"]
 
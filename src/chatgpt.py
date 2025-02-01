import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

class ChatGPT:
    def __init__(self, model: str = "gpt-4"):
        self.api_key = OPENAI_API_KEY
        self.model = model

    def analyze_move(self, board: str, color: str, best_move: str) -> str:
        prompt = f"""I am learning chess and using Stockfish to find the best moves. 
        I am playing as {color}, and I need help understanding why a move is the best.
        I will send you the current board position and the best move suggested by Stockfish for {color}.
        Here is the board representation (lowercase letters are black, uppercase letters are white, and dots represent empty squares): 
        "{board}".
        Stockfish suggests the best move is '{best_move}'.
        Please explain why this is the best move, considering tactics, strategy, and positional factors. 
        Keep your answer concise, under 400 characters."""
        client = OpenAI(api_key=self.api_key)

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "system", "content": "You are a chess tutor helping a student understand moves."},
                      {"role": "user", "content": prompt}],
        )
        
        return response.choices[0].message.content

import chess
import chess.engine
import random
import platform
import os

def get_stockfish_path():
    system = platform.system()
    if system == 'Windows':
        return os.path.join('bin', 'stockfish.exe')
    elif system == 'Darwin':  # macOS
        return os.path.join('bin', 'stockfish-mac')
    elif system == 'Linux':
        return os.path.join('bin', 'stockfish-linux')
    else:
        raise RuntimeError("Unsupported OS for Stockfish")

class ChessGame:
    def __init__(self, player_color='white', player_elo=1200, computer_elo=1500):
        self.board = chess.Board()

        if player_color.lower() not in ['white', 'black']:
            raise ValueError("Color must be 'white' or 'black'")

        self.player_color = chess.WHITE if player_color.lower() == 'white' else chess.BLACK
        self.computer_color = not self.player_color

        self.player_elo = player_elo
        self.computer_elo = computer_elo

        self.engine = chess.engine.SimpleEngine.popen_uci(get_stockfish_path())
        print(f"Game started! You are playing as {'White' if self.player_color == chess.WHITE else 'Black'}.")

    def print_board(self):
        print(self.board)

    def is_game_over(self):
        return self.board.is_game_over()

    def get_result(self):
        if not self.is_game_over():
            return "Game is still in progress."
        return self.board.result()

    def player_move(self, move_uci):
        try:
            move = chess.Move.from_uci(move_uci)
            if move in self.board.legal_moves:
                self.board.push(move)
            else:
                print("Illegal move. Try again.")
        except ValueError:
            print("Invalid move format. Use UCI format like 'e2e4'.")

    def computer_move(self):
        if self.board.is_game_over():
            print("Game over. No move for computer.")
            return

        result = self.engine.play(self.board, chess.engine.Limit(time=0.1))
        self.board.push(result.move)
        print(f"Computer plays: {result.move}")

    def close(self):
        self.engine.quit()
        print("Engine shut down. Thanks for playing!")
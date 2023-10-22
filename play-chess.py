import tkinter as tk
from tkinter import messagebox
import chess
import chess.svg
from PIL import Image, ImageTk
import chess.engine
import subprocess

class ChessGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Chess Game")
        self.board = chess.Board()
        self.captured_pieces = []  # List to store captured pieces
        self.canvas = tk.Canvas(root, width=400, height=400)
        self.canvas.pack()
        self.load_images()
        self.draw_board()
        self.selected_square = None
        self.deselect_timer = None  # Timer for deselection
        self.auto_move_timer = None  # Timer for the computer's move
        self.canvas.bind("<Button-1>", self.on_square_click)
        root.after(2000, self.play_computer_move)  # Initial computer move

    def show_alert(self, message):
        # Use the notify-send command to display a notification
        subprocess.run(["notify-send", "Computer's Turn", message])

    def hide_alert(self):
        # Use the notify-send command to display a notification
        subprocess.run(["notify-send", "Your Turn", "It's your turn!"])

    def load_images(self):
        self.piece_images = {}
        piece_mappings = {
            'r': 'black_rook',
            'n': 'black_knight',
            'b': 'black_bishop',
            'q': 'black_queen',
            'k': 'black_king',
            'p': 'black_pawn',
            'R': 'white_rook',
            'N': 'white_knight',
            'B': 'white_bishop',
            'Q': 'white_queen',
            'K': 'white_king',
            'P': 'white_pawn',
        }
        for piece_symbol, piece_name in piece_mappings.items():
            img = Image.open(f"chess_pieces/{piece_name}.png")
            img = ImageTk.PhotoImage(img.resize((int(50 * 0.7), int(50 * 0.7))))
            self.piece_images[piece_symbol] = img

    def draw_board(self):
        for row in range(8):
            for col in range(8):
                square_color = "white" if (row + col) % 2 == 0 else "gray"
                self.canvas.create_rectangle(col * 50, row * 50, (col + 1) * 50, (row + 1) * 50, fill=square_color)
                piece = self.board.piece_at(chess.square(col, 7 - row))
                if piece is not None:
                    img = self.piece_images[piece.symbol()]
                    self.canvas.create_image(col * 50 + 25, row * 50 + 25, image=img, tags=piece.symbol())

    def on_square_click(self, event):
        if self.deselect_timer:
            return  # If a deselection timer is active, do nothing

        col = event.x // 50
        row = 7 - (event.y // 50)
        square = chess.square(col, row)
        piece = self.board.piece_at(square)

        if self.board.turn == chess.WHITE and piece is not None and piece.color == chess.WHITE:
            if self.selected_square is None:
                self.selected_square = square
        elif self.board.turn == chess.BLACK and piece is not None and piece.color == chess.BLACK:
            if self.selected_square is None:
                self.selected_square = square
        elif self.selected_square is not None:
            move = chess.Move(self.selected_square, square)
            if move in self.board.legal_moves:
                if self.board.piece_at(self.selected_square).piece_type == chess.PAWN and chess.square_rank(square) in [
                    0, 7]:
                    promotion_piece = self.get_highest_ranked_captured_piece()
                    if promotion_piece:
                        self.board.set_piece_at(square, promotion_piece)
                    else:
                        promotion_piece = chess.QUEEN  # Default to promoting to Queen
                        self.board.set_piece_at(square, promotion_piece)
                        self.selected_square = None
                else:
                    self.board.push(move)

                self.canvas.delete("piece")  # Clear the canvas
                self.draw_board()
                self.play_computer_move()  # Trigger the computer move
                self.deselect_timer = self.root.after(8000, self.deselect_squares)  # Set an 8-second deselection timer
                self.selected_square = None  # Deselect the square

    def deselect_squares(self):
        self.selected_square = None
        self.root.after_cancel(self.deselect_timer)
        self.deselect_timer = None

    def get_highest_ranked_captured_piece(self):
        for piece in reversed(self.captured_pieces):
            if piece.piece_type != chess.PAWN:
                return piece
        return None

    def play_computer_move(self):
        # Show the alert message
        self.show_alert("Computer is thinking...")

        if self.board.turn == chess.BLACK:
            with chess.engine.SimpleEngine.popen_uci("/usr/games/stockfish") as engine:
                result = engine.play(self.board, chess.engine.Limit(time=2))
                self.board.push(result.move)
                self.canvas.delete("piece")  # Clear the canvas
                self.draw_board()
                self.auto_move_timer = self.root.after(2000, self.play_computer_move)  # Schedule the next computer move


if __name__ == "__main__":
    root = tk.Tk()
    game = ChessGame(root)
    root.mainloop()

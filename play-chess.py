import tkinter as tk
import chess
import chess.svg
from PIL import Image, ImageTk
from tkinter import simpledialog, messagebox

class ChessGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Chess Game")
        self.board = chess.Board()
        self.canvas = tk.Canvas(root, width=400, height=400)
        self.canvas.pack()
        self.load_images()
        self.draw_board()
        self.selected_square = None
        self.canvas.bind("<Button-1>", self.on_square_click)

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
                    self.canvas.create_image(col * 50 + 25, row * 50 + 25, image=img)

    def promote_pawn(self):
        options = ["Queen", "Rook", "Knight", "Bishop"]
        response = simpledialog.askstring("Promotion", "Choose a promotion (Queen, Rook, Knight, Bishop):", parent=self.root)
        if response in options:
            piece_mapping = {"Queen": "q", "Rook": "r", "Knight": "n", "Bishop": "b"}
            promotion_piece = chess.Piece.from_symbol(piece_mapping[response])
            self.board.set_piece_at(self.promotion_square, promotion_piece)

    def on_square_click(self, event):
        col = event.x // 50
        row = 7 - (event.y // 50)
        square = chess.square(col, row)
        piece = self.board.piece_at(square)

        if self.selected_square is None:
            if piece is not None:
                self.selected_square = square
        else:
            move = chess.Move(self.selected_square, square)
            if move in self.board.legal_moves:
                if self.board.piece_at(self.selected_square).piece_type == chess.PAWN and chess.square_rank(square) in [0, 7]:
                    # Pawn promotion logic
                    self.promotion_square = square
                    self.promote_pawn()
                else:
                    self.board.push(move)

                self.selected_square = None
                self.canvas.delete("piece")  # Clear the canvas
                self.draw_board()
            else:
                self.selected_square = None

if __name__ == "__main__":
    root = tk.Tk()
    game = ChessGame(root)
    root.mainloop()

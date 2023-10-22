import pygame
import chess
import random

# Define the dimensions of the chessboard and the scale factor for chess pieces
CHESSBOARD_SIZE = 800  # Adjust to your preferred size
SQUARE_SIZE = CHESSBOARD_SIZE // 8
PIECE_SCALE = 0.25  # Adjust to your preferred scale (0.25 means 25% of original size)

# Load piece images
piece_images = {}
for piece in chess.PIECE_SYMBOLS:
    for color in ['w', 'b']:
        img = pygame.image.load(f'chess_pieces/{color}{piece}.png')
        img = pygame.transform.scale(img, (int(SQUARE_SIZE * PIECE_SCALE), int(SQUARE_SIZE * PIECE_SCALE)))
        piece_images[chess.BaseBoard.piece_symbol(piece, color)] = img

def draw_chess_board(screen, board):
    for row in range(8):
        for col in range(8):
            square_color = (255, 206, 158) if (row + col) % 2 == 0 else (209, 139, 71)
            pygame.draw.rect(screen, square_color, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
            piece = board.piece_at(chess.square(col, 7 - row))
            if piece:
                screen.blit(piece_images[piece.symbol()], (col * SQUARE_SIZE, (7 - row) * SQUARE_SIZE))

def get_computer_move(board):
    legal_moves = list(board.legal_moves)
    return random.choice(legal_moves)

def play_chess():
    pygame.init()
    screen = pygame.display.set_mode((CHESSBOARD_SIZE, CHESSBOARD_SIZE))
    pygame.display.set_caption("Chess Game")

    board = chess.Board()

    while not board.is_game_over():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

        draw_chess_board(screen, board)
        pygame.display.flip()

        if not board.turn:  # Computer's turn (black)
            move = get_computer_move(board)
            board.push(move)

    pygame.quit()

if __name__ == "__main__":
    print("Welcome to Python Chess!")
    play_chess()

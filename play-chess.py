import pygame
import chess
import random

# Define the dimensions of the chessboard and the scale factor for chess pieces
CHESSBOARD_SIZE = 500  # Adjust to your preferred size
SQUARE_SIZE = CHESSBOARD_SIZE // 8
PIECE_SCALE = 0.88  # Adjust to your preferred scale (0.88 means 88% of original size)

# Define a dictionary to map piece notation to image filenames
piece_image_filenames = {
    'r': 'black_rook.png',
    'n': 'black_knight.png',
    'b': 'black_bishop.png',
    'q': 'black_queen.png',
    'k': 'black_king.png',
    'p': 'black_pawn.png',
    'R': 'white_rook.png',
    'N': 'white_knight.png',
    'B': 'white_bishop.png',
    'Q': 'white_queen.png',
    'K': 'white_king.png',
    'P': 'white_pawn.png',
}


def load_piece_images():
    piece_images = {}
    for piece, filename in piece_image_filenames.items():
        img = pygame.image.load(f'chess_pieces/{filename}')
        img = pygame.transform.scale(img, (int(SQUARE_SIZE * PIECE_SCALE), int(SQUARE_SIZE * PIECE_SCALE)))
        piece_images[piece] = img
    return piece_images


def draw_chess_board(screen, board, piece_images):
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
    piece_images = load_piece_images()

    selected_square = None  # Store the selected square
    move_started = False

    while not board.is_game_over():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.MOUSEBUTTONDOWN:
                col = event.pos[0] // SQUARE_SIZE
                row = 7 - event.pos[1] // SQUARE_SIZE
                square = chess.square(col, row)
                piece = board.piece_at(square)

                if not move_started and piece and piece.color == board.turn:
                    selected_square = square
                    move_started = True
                elif move_started and square != selected_square:
                    move = chess.Move(selected_square, square)
                    if move in board.legal_moves:
                        board.push(move)
                    move_started = False
                else:
                    move_started = False

        draw_chess_board(screen, board, piece_images)
        pygame.display.flip()

        if not board.turn:  # Computer's turn (black)
            move = get_computer_move(board)
            board.push(move)

    pygame.quit()


if __name__ == "__main__":
    print("Welcome to Python Chess!")
    play_chess()

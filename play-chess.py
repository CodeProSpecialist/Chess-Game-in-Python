import chess

def print_board(board):
    print(board)

def print_menu():
    print("Chess Game Menu:")
    print("1. Start New Chess Game")
    print("2. Exit")

def start_chess():
    board = chess.Board()
    print("Starting a new standard chess game.")
    while not board.is_game_over():
        print_board(board)
        move = input("Enter your move (e.g., 'e2e4'): ")
        try:
            board.push_san(move)
        except ValueError:
            print("Invalid move. Try again.")
    print("Game over!")

def main():
    print("Welcome to Python Chess!")

    while True:
        print_menu()
        choice = input("Enter your choice: ")
        if choice == '1':
            start_chess()
        elif choice == '2':
            break
        else:
            print("Invalid choice. Please select 1 or 2.")

if __name__ == "__main__":
    main()

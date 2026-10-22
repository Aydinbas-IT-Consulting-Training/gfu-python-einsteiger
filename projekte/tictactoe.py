"""Tic-Tac-Toe für zwei Spieler im Terminal (Lösung zu Notebook 10).

Nach Inden, *Einstieg in Python*, Kapitel 13.

Start: ``uv run python projekte/tictactoe.py``
"""

EMPTY = " "
Board = list[list[str]]


def create_board() -> Board:
    return [[EMPTY for _ in range(3)] for _ in range(3)]


def print_board(board: Board) -> None:
    for row_index, row in enumerate(board):
        print(" " + " | ".join(row))
        if row_index < 2:
            print("---+---+---")


def place_mark(board: Board, field: int, mark: str) -> None:
    if not 1 <= field <= 9:
        raise ValueError(f"Feld {field} gibt es nicht")
    row, col = divmod(field - 1, 3)
    if board[row][col] != EMPTY:
        raise ValueError(f"Feld {field} ist schon belegt")
    board[row][col] = mark


def has_won(board: Board, mark: str) -> bool:
    lines = []
    lines.extend(board)
    lines.extend([[board[row][col] for row in range(3)] for col in range(3)])
    lines.append([board[i][i] for i in range(3)])
    lines.append([board[i][2 - i] for i in range(3)])
    return any(line == [mark, mark, mark] for line in lines)


def is_full(board: Board) -> bool:
    return all(cell != EMPTY for row in board for cell in row)


def ask_for_field(mark: str) -> int:
    while True:
        answer = input(f"Spieler {mark}, welches Feld (1-9)? ")
        try:
            return int(answer)
        except ValueError:
            print(f"'{answer}' ist keine Zahl")


def play() -> None:
    board = create_board()
    mark = "X"
    while True:
        print_board(board)
        try:
            place_mark(board, ask_for_field(mark), mark)
        except ValueError as error:
            print(error)
            continue

        if has_won(board, mark):
            print_board(board)
            print(f"Spieler {mark} gewinnt!")
            return
        if is_full(board):
            print_board(board)
            print("Unentschieden!")
            return
        mark = "O" if mark == "X" else "X"


def main() -> None:
    play()


if __name__ == "__main__":
    main()

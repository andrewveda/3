import csv
import json
import os
from collections import defaultdict

BOARD_FILES = "abcdefgh"

PIECES = {
    "P": "pawn",
    "N": "knight",
    "B": "bishop",
    "R": "rook",
    "Q": "queen",
    "K": "king",
    "p": "pawn",
    "n": "knight",
    "b": "bishop",
    "r": "rook",
    "q": "queen",
    "k": "king",
}

MAX_PER_FILE = 5000

OUTPUT = "output"

for p in ["pawn","knight","bishop","rook","queen","king"]:
    os.makedirs(os.path.join(OUTPUT, p), exist_ok=True)


def fen_to_board(fen):
    board = {}
    rows = fen.split()[0].split("/")

    for r, row in enumerate(rows):
        file = 0
        rank = 8 - r

        for c in row:
            if c.isdigit():
                file += int(c)
            else:
                square = BOARD_FILES[file] + str(rank)
                board[square] = c
                file += 1

    return board


def square(move):
    return move[:2], move[2:4]


def piece_from_first_move(fen, move):
    board = fen_to_board(fen)

    src, dst = square(move)

    piece = board.get(src)

    if piece:
        return PIECES[piece]

    return None
buffers = defaultdict(list)
part = defaultdict(lambda: 1)


def flush(piece):
    if not buffers[piece]:
        return

    folder = os.path.join(OUTPUT, piece)

    filename = os.path.join(
        folder,
        f"part{part[piece]:04d}.json"
    )

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(buffers[piece], f, ensure_ascii=False)

    buffers[piece].clear()
    part[piece] += 1


with open("lichess_db_puzzle.csv", newline="", encoding="utf-8") as f:

    reader = csv.DictReader(f)

    for row in reader:

        moves = row["Moves"].split()

        piece = piece_from_first_move(
            row["FEN"],
            moves[0]
        )

        if piece is None:
            continue

        puzzle = {
            "puzzleId": row["PuzzleId"],
            "fen": row["FEN"],
            "moves": moves,
            "rating": int(row["Rating"]),
            "ratingDeviation": int(row["RatingDeviation"]),
            "popularity": int(row["Popularity"]),
            "nbPlays": int(row["NbPlays"]),
            "themes": row["Themes"].split(),
            "gameUrl": row["GameUrl"],
            "openingTags": row["OpeningTags"].split()
        }

        buffers[piece].append(puzzle)

        if len(buffers[piece]) >= MAX_PER_FILE:
            flush(piece)

for p in buffers:
    flush(p)

print("Done.")
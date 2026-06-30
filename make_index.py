import os
import json

ROOT = "output"

index = {}

for piece in ["pawn", "knight", "bishop", "rook", "queen", "king"]:
    folder = os.path.join(ROOT, piece)

    files = sorted(
        f for f in os.listdir(folder)
        if f.endswith(".json")
    )

    index[piece] = files

with open(os.path.join(ROOT, "index.json"), "w") as f:
    json.dump(index, f, indent=2)

print("index.json created")
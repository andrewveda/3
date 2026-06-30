import os
import json

ROOT = "output"

master = {}

for piece in ["pawn", "knight", "bishop", "rook", "queen", "king"]:

    folder = os.path.join(ROOT, piece)

    files = sorted(
        f for f in os.listdir(folder)
        if f.endswith(".json")
    )

    # Per-piece index
    with open(os.path.join(folder, "index.json"), "w") as f:
        json.dump(files, f, indent=2)

    # Master index
    master[piece] = files

# Master index
with open(os.path.join(ROOT, "index.json"), "w") as f:
    json.dump(master, f, indent=2)

print("Done.")
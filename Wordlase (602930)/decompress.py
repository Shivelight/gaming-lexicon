import argparse
import json
import zlib
from os.path import basename


def main():
    parser = argparse.ArgumentParser(description="Decompress Wordlase dictionary file.")
    parser.add_argument(
        "file",
        help="Path to the dictionary to decompress (e.g. E:\\SteamLibrary\\steamapps\\common\\Wordlase\\data\\en.dat)",
    )
    args = parser.parse_args()

    target = basename(args.file) + ".json"

    with open(args.file, "rb") as f:
        gamedata = json.loads(zlib.decompress(f.read()))

    # sort answers from shortest to longest
    for key in gamedata["game"]:
        gamedata["game"][key].sort(key=len)

    with open(target, "w", encoding="utf-8") as f:
        json.dump(gamedata["game"], f, indent=2)
        print(f"Result written to {target}")


if __name__ == "__main__":
    main()

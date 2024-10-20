import argparse
import struct
from os.path import basename


def read_n_chars(f, num_chars):
    chars = []
    buf = b""
    while len(chars) < num_chars:
        buf += f.read(1)
        if not buf:
            raise ValueError(
                f"Unexpected end of file while reading characters. Expected {num_chars}, got {len(chars)}."
            )
        try:
            chars.append(buf.decode("utf-8", errors="strict"))
            buf = b""
        except UnicodeDecodeError:
            pass

    return "".join(chars)


def parse_binary_file(file_path):
    words = []

    with open(file_path, "rb") as f:
        while True:
            length_bytes = f.read(2)
            if not length_bytes:
                break

            word_length = struct.unpack("<H", length_bytes)[0]
            word = read_n_chars(f, word_length)
            words.append(word)

    return words


def main():
    parser = argparse.ArgumentParser(description="Parse Ace Of Word dictionary file.")
    parser.add_argument(
        "file",
        help="Path to the dictionary to parse (e.g. E:\\SteamLibrary\\steamapps\\common\\AceOfWords\\content\\messages\\US_4_final.bin)",
    )
    args = parser.parse_args()

    parsed_words = parse_binary_file(args.file)
    target = basename(args.file) + ".txt"

    with open(target, "w", encoding="utf-8") as f:
        f.write("\n".join(parsed_words))
        print(f"Result written to {target}")


if __name__ == "__main__":
    main()

import argparse
from os.path import basename


class Trie:
    """
    Trie class for Obliteracy dictionary file. Format is reverse engineered.
    """

    def __init__(self):
        self.first_child = None
        self.next_sibling = None
        self.source_byte = 0

    def get_letter(self) -> str:
        return chr((self.source_byte % 32) + 65)

    def is_word(self) -> bool:
        return bool(self.source_byte & 0x20)

    def add_word(self, byte_array: bytearray):
        try:
            self.source_byte = byte_array.pop(0)
        except IndexError:
            return None

        # Check if the node has a first child
        if self.source_byte & 0x40:
            self.first_child = Trie()
            self.first_child.add_word(byte_array)

        # Check if the node has a sibling
        if self.source_byte & 0x80:
            self.next_sibling = None
        else:
            self.next_sibling = Trie()
            self.next_sibling.add_word(byte_array)

        return self

    def get_all_words(self, current_word="", first=True):
        words = []
        node = self

        while node is not None:
            current_letter = node.get_letter()

            # skip first (it's just an "A")
            if first:
                new_word = current_word
            else:
                new_word = current_word + current_letter

            if node.is_word():
                words.append(new_word)

            # If the node has a first child, recursively collect words from the child
            if node.first_child is not None:
                words.extend(node.first_child.get_all_words(new_word, False))

            node = node.next_sibling

        return words


def parse_dictionary(file_path):
    root = Trie()
    with open(file_path, "rb") as f:
        root.add_word(bytearray(f.read()))

    return root


def main():
    parser = argparse.ArgumentParser(description="Parse Obliteracy dictionary file.")
    parser.add_argument(
        "file",
        help="Path to the dictionary to parse (e.g. E:\\SteamLibrary\\steamapps\\common\\Obliteracy\\data\\dict\\dictionary.dat)",
    )
    args = parser.parse_args()

    root = parse_dictionary(args.file)
    target = basename(args.file) + ".txt"

    with open(target, "w", encoding="utf-8") as f:
        f.write("\n".join(root.get_all_words()))
        print(f"Result written to {target}")


if __name__ == "__main__":
    main()

import argparse


MORSE_DICT = {
    'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..',
    'E': '.', 'F': '..-.', 'G': '--.', 'H': '....', 
    'I': '..', 'J': '.---', 'K': '-.-', 'L': '.-..', 
    'M': '--', 'N': '-.', 'O': '---', 'P': '.--.',
    'Q': '--.-', 'R': '.-.', 'S': '...', 'T': '-',
    'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-', 
    'Y': '-.--', 'Z': '--..',
    '1': '.----', '2': '..---', '3': '...--', 
    '4': '....-', '5': '.....', '6': '-....',
    '7': '--...', '8': '---..', '9': '----.',
    '0': '-----', ',': '--..--', '.': '.-.-.-',
    '?': '..--..', '/': '-..-.', '-': '-....-', 
    '(': '-.--.', ')': '-.--.-'
}

REVERSE = {code: char for char, code in MORSE_DICT.items()}

def encode(text):
    """Encode a text to morse code."""
    words = []

    for word in text.upper().split():
        letters = []
        for char in word:
            if char not in MORSE_DICT:
                raise ValueError(f"Character '{char}' cannot be encoded.")
            letters.append(MORSE_DICT[char])
        words.append(" ".join(letters))

    return " / ".join(words)

def decode(morse):
    """Decode morse code to text"""

    words = []

    for word in morse.split("/"):
        letters = []
        for code in word.split():
            if code not in REVERSE:
                raise ValueError(f"Morse code '{code}' cannot be decoded.")
            letters.append(REVERSE[code])
        # to prevent adding empty words incase there are trailing spaces.
        if letters:
            words.append("".join(letters))
    return " ".join(words)


def timing_sequence(morse):
    """
    Turn Morse code into a list (is_on, units) pairs using the standard timing.
    dot = 1 unit on
    dash = 3 units on
    gap btw symbols = 1 unit off
    gap btw letters = 3 units off
    gap btw words = 7 units off
    """
    sequence = []

    words = [w.split() for w in morse.split("/") if w.strip()]

    for word_index, letters in enumerate(words):
        if word_index>0:
            sequence.append((False, 7))  # gap between words

        for letter_index, code in enumerate(letters):
            if letter_index>0:
                sequence.append((False, 3))  # gap between letters
            



def main():
    parser = argparse.ArgumentParser(description="A morse code convertor tool!")
    subparsers = parser.add_subparsers(dest="command", required=True)

    enc = subparsers.add_parser("encode", help="Encode a text to morse code")
    enc.add_argument("text", nargs="+", type=str, help="Text to encode")

    dec = subparsers.add_parser("decode", help="Decode morse code to text")
    dec.add_argument("morse", nargs="+", type=str, help="Morse code to decode")


    args = parser.parse_args()
    if args.command == "encode":
        print(encode(" ".join(args.text)))
    elif args.command == "decode":
        print(decode(" ".join(args.morse)))

if __name__ == "__main__":
    main()
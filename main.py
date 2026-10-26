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
    '0': '-----', ', ': '--..--', '.': '.-.-.-',
    '?': '..__..', '/': '-..-.', '-': '-....-', 
    '(': '-.--.', ')': '-.--.-', ' ': '/'
}

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
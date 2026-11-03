import argparse
import math
import struct
import wave


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


def write_wav(morse, path, wpm=15, frequency=600, sample_rate=8000):
    """
    Write Morse code to the beeps in wav files. return the number of samples.
    """
    unit_duration = 1.2/wpm
    unit_frames = int(unit_duration * sample_rate)

    with wave.open(path, 'wb') as wav_file:
        wav_file.setnchannels(1)  # mono
        wav_file.setsampwidth(2)  # 2 bytes per sample
        wav_file.setframerate(sample_rate)

        audio_samples = bytearray()
        sample_index = 0 #position across entire audio

        for is_on, units in timing_sequence(morse):

            total_frames = units*unit_frames

            for i in range(total_frames):
                if is_on:
                    t = sample_index/sample_rate
                    sine_wave = int(32767.0*math.sin(2.0*math.pi*frequency*t))
                    audio_samples+=struct.pack('<h', sine_wave)
                else:
                    audio_samples+=struct.pack('<h', 0)
                sample_index += 1

        wav_file.writeframes(audio_samples)

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

            for symbol_index, symbol in enumerate(code):
                if symbol_index>0:
                    sequence.append((False, 1))  # gap between symbols

                if symbol == ".":
                    sequence.append((True, 1))  # dot
                elif symbol == "-":
                    sequence.append((True, 3))  # dash
                else:
                    raise ValueError(f"Invalid Morse code symbol: '{symbol}'")
    return sequence
            





def main():
    parser = argparse.ArgumentParser(description="A morse code convertor tool!")
    subparsers = parser.add_subparsers(dest="command", required=True)

    enc = subparsers.add_parser("encode", help="Encode a text to morse code")
    enc.add_argument("text", nargs="+", type=str, help="Text to encode")

    dec = subparsers.add_parser("decode", help="Decode morse code to text")
    dec.add_argument("morse", nargs="+", type=str, help="Morse code to decode")

    tim = subparsers.add_parser("timing", help="Generate timing sequence from morse code")
    tim.add_argument("morse", nargs="+", type=str, help="Morse code to process")

    args = parser.parse_args()
    if args.command == "encode":
        print(encode(" ".join(args.text)))
    elif args.command == "decode":
        print(decode(" ".join(args.morse)))
    elif args.command == "timing":
        print(timing_sequence(" ".join(args.morse)))

    

if __name__ == "__main__":
    main()
import string

def encrypt_char(ch, shift1, shift2):
    if ch.islower():
        if 'a' <= ch <= 'm':
            shift = shift1 * shift2
            return chr((ord(ch) - ord('a') + shift) % 26 + ord('a'))
        elif 'n' <= ch <= 'z':
            shift = -(shift1 + shift2)
            return chr((ord(ch) - ord('a') + shift) % 26 + ord('a'))
    elif ch.isupper():
        if 'A' <= ch <= 'M':
            shift = -shift1
            return chr((ord(ch) - ord('A') + shift) % 26 + ord('A'))
        elif 'N' <= ch <= 'Z':
            shift = shift2 ** 2
            return chr((ord(ch) - ord('A') + shift) % 26 + ord('A'))
    return ch

def encrypt_file(input_file, output_file, shift1, shift2):
    with open(input_file, "r") as f:
        text = f.read()
    encrypted = "".join(encrypt_char(ch, shift1, shift2) for ch in text)
    with open(output_file, "w") as f:
        f.write(encrypted)

def decrypt_char(ch, shift1, shift2):
    if ch.islower():
        if 'a' <= ch <= 'm':
            shift = -(shift1 * shift2)
            return chr((ord(ch) - ord('a') + shift) % 26 + ord('a'))
        elif 'n' <= ch <= 'z':
            shift = (shift1 + shift2)
            return chr((ord(ch) - ord('a') + shift) % 26 + ord('a'))
    elif ch.isupper():
        if 'A' <= ch <= 'M':
            shift = shift1
            return chr((ord(ch) - ord('A') + shift) % 26 + ord('A'))
        elif 'N' <= ch <= 'Z':
            shift = -(shift2 ** 2)
            return chr((ord(ch) - ord('A') + shift) % 26 + ord('A'))
    return ch

def decrypt_file(input_file, output_file, shift1, shift2):
    with open(input_file, "r") as f:
        text = f.read()
    decrypted = "".join(decrypt_char(ch, shift1, shift2) for ch in text)
    with open(output_file, "w") as f:
        f.write(decrypted)

def verify(original_file, decrypted_file):
    with open(original_file, "r") as f1, open(decrypted_file, "r") as f2:
        if f1.read() == f2.read():
            print("✅ Decryption successful! Files match.")
        else:
            print("❌ Decryption failed! Files do not match.")

if __name__ == "__main__":
    shift1 = int(input("Enter shift1: "))
    shift2 = int(input("Enter shift2: "))
    encrypt_file("raw_text.txt", "encrypted_text.txt", shift1, shift2)
    decrypt_file("encrypted_text.txt", "decrypted_text.txt", shift1, shift2)
    verify("raw_text.txt", "decrypted_text.txt")

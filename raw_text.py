def encrypt_char(ch, s1, s2):
    if ch.islower():
        if ch <= 'm':  # first half a-m
            return chr((ord(ch) - ord('a') + s1 * s2) % 26 + ord('a'))
        else:          # n-z
            return chr((ord(ch) - ord('a') - (s1 + s2)) % 26 + ord('a'))
    elif ch.isupper():
        if ch <= 'M':  # first half A-M
            return chr((ord(ch) - ord('A') - s1) % 26 + ord('A'))
        else:          # N-Z
            return chr((ord(ch) - ord('A') + (s2 ** 2)) % 26 + ord('A'))
    else:
        return ch  # keep numbers, spaces, symbols


def decrypt_char(ch, s1, s2):
    if ch.islower():
        if ch <= 'm':
            return chr((ord(ch) - ord('a') - s1 * s2) % 26 + ord('a'))
        else:
            return chr((ord(ch) - ord('a') + (s1 + s2)) % 26 + ord('a'))
    elif ch.isupper():
        if ch <= 'M':
            return chr((ord(ch) - ord('A') + s1) % 26 + ord('A'))
        else:
            return chr((ord(ch) - ord('A') - (s2 ** 2)) % 26 + ord('A'))
    else:
        return ch


def encrypt_file(s1, s2):
    with open("raw_text.txt", "r", encoding="utf-8") as f:
        text = f.read()
    encrypted = "".join(encrypt_char(c, s1, s2) for c in text)
    with open("encrypted_text.txt", "w", encoding="utf-8") as f:
        f.write(encrypted)


def decrypt_file(s1, s2):
    with open("encrypted_text.txt", "r", encoding="utf-8") as f:
        text = f.read()
    decrypted = "".join(decrypt_char(c, s1, s2) for c in text)
    with open("decrypted_text.txt", "w", encoding="utf-8") as f:
        f.write(decrypted)


def verify():
    with open("raw_text.txt", "r", encoding="utf-8") as f1, open("decrypted_text.txt", "r", encoding="utf-8") as f2:
        return f1.read() == f2.read()


# Main
s1 = int(input("Enter shift1: "))
s2 = int(input("Enter shift2: "))

encrypt_file(s1, s2)
decrypt_file(s1, s2)

if verify():
    print("✅ Decryption successful!")
else:
    print("❌ Decryption failed.")

def caesar_cipher(text, shift):
    """Shift each alphabetic character by a given number of positions."""
    result = []
    shift = shift % 26

    for char in text:
        if char.isalpha():
            start = ord('A') if char.isupper() else ord('a')
            offset = ord(char) - start
            new_offset = (offset + shift) % 26
            result.append(chr(start + new_offset))
        else:
            result.append(char)

    return "".join(result)


def caesar_decipher(cyphertext, shift):
    """Decrypt a Caesar-ciphered string by shifting backward."""
    return caesar_cipher(cyphertext, -shift)


def letter_frequency(text):
    """Return the count of each letter from a to z in the given text."""
    counts = {chr(ord('a') + i): 0 for i in range(26)}

    for char in text:
        if char.isalpha():
            letter = char.lower()
            counts[letter] += 1

    return counts


def main():
    while True:
        print("\nCaesar Cipher Menu")
        print("1. Encrypt and analyze a message")
        print("2. Decrypt a message")
        print("3. Exit")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            message = input("Enter a message: ")
            shift = int(input("Enter a shift value: "))

            encrypted = caesar_cipher(message, shift)
            frequencies = letter_frequency(message)
            decrypted = caesar_decipher(encrypted, shift)

            print("\nEncrypted text:", encrypted)
            print("Letter frequency:")
            for letter, count in frequencies.items():
                if count > 0:
                    print(f"  {letter}: {count}")
            print("Decrypted text:", decrypted)

        elif choice == "2":
            message = input("Enter the encrypted message: ")
            shift = int(input("Enter the shift value: "))
            original = caesar_decipher(message, shift)
            print("\nOriginal text:", original)

        elif choice == "3":
            print("Goodbye!")
            break

        else:
            print("Invalid choice. Please choose 1, 2, or 3.")


if __name__ == "__main__":
    main()

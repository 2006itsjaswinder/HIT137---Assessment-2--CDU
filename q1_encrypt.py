import os
from pathlib import Path

def encrypt(text, shift1, shift2):
    encrypted = ""
    for i, char in enumerate(text):
        if char.isalpha():
            shift = shift1 if i % 2 == 0 else shift2
            base = ord('A') if char.isupper() else ord('a')
            encrypted += chr((ord(char) - base + shift) % 26 + base)
        else:
            encrypted += char
    return encrypted

def decrypt(text, shift1, shift2):
    decrypted = ""
    for i, char in enumerate(text):
        if char.isalpha():
            shift = shift1 if i % 2 == 0 else shift2
            base = ord('A') if char.isupper() else ord('a')
            decrypted += chr((ord(char) - base - shift) % 26 + base)
        else:
            decrypted += char
    return decrypted

# Paths
base_path = Path(__file__).parent
output_folder = base_path / "q1_output"
output_folder.mkdir(exist_ok=True)  # Create output folder if not exists

file_name = base_path / "raw_text.txt"
if not file_name.exists():
    raise FileNotFoundError(f"Input file not found: {file_name}")

with open(file_name, "r") as f:
    original_text = f.read()

shift1 = int(input("Enter first shift: "))
shift2 = int(input("Enter second shift: "))

encrypted_text = encrypt(original_text, shift1, shift2)
decrypted_text = decrypt(encrypted_text, shift1, shift2)

print("\nEncrypted:\n", encrypted_text)
print("\nDecrypted:\n", decrypted_text)

# Save results to output folder
with open(output_folder / "encrypted.txt", "w") as f:
    f.write(encrypted_text)
with open(output_folder / "decrypted.txt", "w") as f:
    f.write(decrypted_text)

print("\nVerification:", "Success" if decrypted_text == original_text else "Failed")
print(f"\nFiles saved in: {output_folder}")

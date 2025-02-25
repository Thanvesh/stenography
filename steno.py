"""import cv2
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt

def encode_message(image_path, secret_message, output_path):
    # Load the image
    image = cv2.imread(image_path)
    if image is None:
        raise ValueError("Image not found or unable to load.")
    
    # Convert image to RGB (OpenCV loads images in BGR by default)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    
    # Convert message to binary
    binary_message = ''.join(format(ord(char), '08b') for char in secret_message) + '1111111111111110'  # End delimiter
    
    data_index = 0
    message_length = len(binary_message)
    
    # Encode the message into the image
    for row in image:
        for pixel in row:
            for i in range(3):  # Iterate over R, G, B channels
                if data_index < message_length:
                    pixel[i] = (pixel[i] & 0xFE) | int(binary_message[data_index])
                    data_index += 1
                else:
                    break
    
    # Save the encoded image
    encoded_image = Image.fromarray(image)
    encoded_image.save(output_path)
    print(f"Message encoded and saved as {output_path}")

def decode_message(image_path):
    # Load the image
    image = cv2.imread(image_path)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    binary_message = ""

    for row in image:
        for pixel in row:
            for i in range(3):  # Extract from R, G, B channels
                binary_message += str(pixel[i] & 1)

    # Find the end delimiter (1111111111111110)
    end_index = binary_message.find("1111111111111110")
    if end_index != -1:
        binary_message = binary_message[:end_index]  # Remove the delimiter
    
    # Convert binary to text
    chars = [binary_message[i:i+8] for i in range(0, len(binary_message), 8)]
    decoded_text = "".join(chr(int(char, 2)) for char in chars)

    print("Decoded Message:", decoded_text)
    return decoded_text

def display_images(original_path, encoded_path):
    original = Image.open(original_path)
    encoded = Image.open(encoded_path)
    
    plt.figure(figsize=(10,5))
    
    plt.subplot(1,2,1)
    plt.title("Original Image")
    plt.imshow(original)
    plt.axis("off")
    
    plt.subplot(1,2,2)
    plt.title("Encoded Image")
    plt.imshow(encoded)
    plt.axis("off")
    
    plt.show()

# Example usage
original_image = "D:\\NxtWaveProjects\\stenography\\images\\Pngtree.png"
encoded_image = "D:\\NxtWaveProjects\\stenography\\images\\encoded.png"
secret_text = "This is a secret!"

encode_message(original_image, secret_text, encoded_image)
decoded_text = decode_message(encoded_image)
display_images(original_image, encoded_image)

print("Hidden Message:", decoded_text)
"""

import cv2
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
from Crypto.Cipher import AES
import base64

# Function to pad the message to be a multiple of 16 bytes (AES block size)
def pad_message(message):
    return message + (16 - len(message) % 16) * chr(16 - len(message) % 16)

# Function to encrypt the message using AES
def encrypt_message(secret_message, key):
    cipher = AES.new(key, AES.MODE_ECB)
    padded_message = pad_message(secret_message)
    encrypted_message = cipher.encrypt(padded_message.encode())
    return base64.b64encode(encrypted_message).decode()  # Convert to base64 for easier storage

# Function to decrypt the extracted message
def decrypt_message(encrypted_message, key):
    cipher = AES.new(key, AES.MODE_ECB)
    encrypted_message = base64.b64decode(encrypted_message)
    decrypted_message = cipher.decrypt(encrypted_message).decode()
    return decrypted_message.rstrip(chr(16 - len(decrypted_message) % 16))  # Remove padding

def encode_message(image_path, secret_message, output_path, key):
    # Encrypt the message
    encrypted_message = encrypt_message(secret_message, key)
    
    # Load the image
    image = cv2.imread(image_path)
    if image is None:
        raise ValueError("Image not found or unable to load.")
    
    # Convert image to RGB (OpenCV loads images in BGR by default)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    
    # Convert encrypted message to binary
    binary_message = ''.join(format(ord(char), '08b') for char in encrypted_message) + '1111111111111110'  # End delimiter
    
    data_index = 0
    message_length = len(binary_message)
    
    # Encode the message into the image
    for row in image:
        for pixel in row:
            for i in range(3):  # Iterate over R, G, B channels
                if data_index < message_length:
                    pixel[i] = (pixel[i] & 0xFE) | int(binary_message[data_index])
                    data_index += 1
                else:
                    break
    
    # Save the encoded image
    encoded_image = Image.fromarray(image)
    encoded_image.save(output_path)
    print(f"Encrypted message encoded and saved as {output_path}")

def decode_message(image_path, key):
    # Load the image
    image = cv2.imread(image_path)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    binary_message = ""

    for row in image:
        for pixel in row:
            for i in range(3):  # Extract from R, G, B channels
                binary_message += str(pixel[i] & 1)

    # Find the end delimiter (1111111111111110)
    end_index = binary_message.find("1111111111111110")
    if end_index != -1:
        binary_message = binary_message[:end_index]  # Remove the delimiter
    
    # Convert binary to text
    chars = [binary_message[i:i+8] for i in range(0, len(binary_message), 8)]
    encrypted_text = "".join(chr(int(char, 2)) for char in chars)

    # Decrypt the message
    decrypted_text = decrypt_message(encrypted_text, key)

    print("Decrypted Message:", decrypted_text)
    return decrypted_text

def display_images(original_path, encoded_path):
    original = Image.open(original_path)
    encoded = Image.open(encoded_path)
    
    plt.figure(figsize=(10,5))
    
    plt.subplot(1,2,1)
    plt.title("Original Image")
    plt.imshow(original)
    plt.axis("off")
    
    plt.subplot(1,2,2)
    plt.title("Encoded Image")
    plt.imshow(encoded)
    plt.axis("off")
    
    plt.show()

# Example usage
original_image = "D:\\NxtWaveProjects\\stenography\\images\\Pngtree.png"
encoded_image = "D:\\NxtWaveProjects\\stenography\\images\\encoded.png"
secret_text = "This is a highly secure secret!"
encryption_key = b'16charSecretKey!'  # Ensure exactly 16, 24, or 32 bytes
encode_message(original_image, secret_text, encoded_image, encryption_key)
decoded_text = decode_message(encoded_image, encryption_key)
display_images(original_image, encoded_image)

print("Final Decrypted Hidden Message:", decoded_text)

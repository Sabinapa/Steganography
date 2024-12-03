from PIL import Image
import numpy as np

#1. STEP
def binarize_message(message):
    """Convert the message to binary and prepend its length."""
    binary_message = ''.join(format(ord(char), '08b') for char in message)  # Convert to binary
    size = len(binary_message)  # Length of binary message
    size_binary = f'{size:032b}'  # Convert length to 32-bit binary
    return size_binary + binary_message


# Example message
message = "Hello"
binary_message = binarize_message(message)
print(f"Binarized message: {binary_message}")
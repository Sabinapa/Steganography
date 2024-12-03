from PIL import Image
import numpy as np

#1. STEP
def binarize_message(message):
    """Convert the message to binary and prepend its length."""
    binary_message = ''.join(format(ord(char), '08b') for char in message)  # Convert to binary
    size = len(binary_message)  # Length of binary message
    size_binary = f'{size:032b}'  # Convert length to 32-bit binary
    return size_binary + binary_message

#2. STEP
def split_into_blocks(image_path):
    """Split grayscale image into 8x8 pixel blocks."""
    image = Image.open(image_path).convert('L')  # Convert image to grayscale
    pixels = np.array(image)  # Convert image to NumPy array
    height, width = pixels.shape

    # Divide into 8x8 blocks
    blocks = [
        pixels[i:i + 8, j:j + 8]
        for i in range(0, height, 8)
        for j in range(0, width, 8)
    ]
    return blocks, height, width

"""
# Example message
message = "Hello"
binary_message = binarize_message(message)
print(f"Binarized message: {binary_message}")
"""

image_path = "slike BMP/Baboon.bmp"

blocks, height, width = split_into_blocks(image_path)
print(f"Image dimensions: {height}x{width}")
print(f"Number of 8x8 blocks: {len(blocks)}")
print(f"First block:\n{blocks[0]}")
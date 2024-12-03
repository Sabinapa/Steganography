from PIL import Image
import numpy as np

#1. STEP
"""Convert the message to binary and prepend its length."""
def binarize_message(message):

    binary_message = ''.join(format(ord(char), '08b') for char in message)  # Convert to binary
    size = len(binary_message)  # Length of binary message
    size_binary = f'{size:032b}'  # Convert length to 32-bit binary
    return size_binary + binary_message

#2. STEP
"""Split grayscale image into 8x8 pixel blocks."""
def split_into_blocks(image_path):
    image = Image.open(image_path).convert('L')  # Convert image to grayscale
    pixels = np.array(image)  # Convert image to NumPy array
    height, width = pixels.shape

    # Divide into 8x8 blocks
    blocks = [
        pixels[i:i + 8, j:j + 8]
        for i in range(0, height, 8)
        for j in range(0, width, 8)
    ]
    return blocks, height, width #bloks first blokc, image demensions hegiht, number of 8x8 bloks len(blocks)

#3 STEP
"""Apply Haar transform to an 8x8 block."""
def haar_transform(block):
    transformed = np.zeros_like(block, dtype=float)
    n = block.shape[0]
    while n > 1:
        half = n // 2
        transformed[:half, :half] = (block[:n:2, :n:2] + block[1:n:2, :n:2] + block[:n:2, 1:n:2] + block[1:n:2, 1:n:2]) / 4
        transformed[:half, half:n] = (block[:n:2, :n:2] - block[1:n:2, :n:2] + block[:n:2, 1:n:2] - block[1:n:2, 1:n:2]) / 4
        transformed[half:n, :half] = (block[:n:2, :n:2] + block[1:n:2, :n:2] - block[:n:2, 1:n:2] - block[1:n:2, 1:n:2]) / 4
        transformed[half:n, half:n] = (block[:n:2, :n:2] - block[1:n:2, :n:2] - block[:n:2, 1:n:2] + block[1:n:2, 1:n:2]) / 4
        n = half
    return transformed



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

first_block = blocks[0]
haar_transformed = haar_transform(first_block)
print(f"Haar transformed block:\n{haar_transformed}")
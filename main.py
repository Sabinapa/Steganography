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

#3. STEP
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

#4. STEP
"""Perform zigzag serialization of an 8x8 block."""
def zigzag(block):
    rows, cols = block.shape
    solution = [[] for _ in range(rows + cols - 1)]
    for i in range(rows):
        for j in range(cols):
            solution[i + j].append(block[i][j])
    result = []
    for index, arr in enumerate(solution):
        if index % 2 == 0:
            result.extend(arr[::-1])  # Reverse for zigzag order
        else:
            result.extend(arr)
    return np.array(result)

#5. STEP
"""Quantize coefficients and set the last N to 0."""
def quantize_and_zero_out(coefficients, n):
    quantized = np.round(coefficients)  # Quantize coefficients to integers
    quantized[-n:] = 0  # Set the last N coefficients to 0
    return quantized



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

zigzag_serialized = zigzag(haar_transformed)
print(f"Zigzag serialized coefficients:\n{zigzag_serialized}")

N = 10
quantized_coefficients = quantize_and_zero_out(zigzag_serialized, N)
print(f"Quantized coefficients with last {N} set to 0:\n{quantized_coefficients}")

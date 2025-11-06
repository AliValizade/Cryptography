import random
from Crypto.Cipher import DES
import pandas as pd
import matplotlib.pyplot as plt

def flip_random_bit(byte_string):
    """
    Takes a byte string and flips a single random bit.
    Returns the new byte string and the 0-indexed position of the flipped bit.
    """
    total_bits = len(byte_string) * 8
    # Choose a random bit position (e.g., 0 to 63)
    bit_pos = random.randint(0, total_bits - 1)
    
    # Determine which byte and which bit within that byte
    byte_index = bit_pos // 8
    bit_in_byte = bit_pos % 8
    
    # Create a mask to flip that specific bit
    mask = 1 << bit_in_byte
    
    # Convert immutable bytes to mutable bytearray
    data = bytearray(byte_string)
    
    # Flip the bit using XOR
    data[byte_index] ^= mask
    
    # Convert back to immutable bytes
    return bytes(data), bit_pos

def hamming_distance(bytes1, bytes2):
    """
    Calculates the Hamming distance (number of differing bits)
    between two byte strings of equal length.
    """
    # XOR the two byte strings
    xor_result = bytes(b1 ^ b2 for b1, b2 in zip(bytes1, bytes2))
    
    # Count the number of '1's in the binary representation
    bit_diff_count = 0
    for byte in xor_result:
        bit_diff_count += bin(byte).count('1')
    return bit_diff_count

# --- 1. Base Setup ---
original_key = b'mysecret'  # 8-byte key
original_plaintext = b'\x00\x00\x00\x00\x00\x00\x00\x00' # 8-byte plaintext
cipher = DES.new(original_key, DES.MODE_ECB)

# Encrypt the original data
original_ciphertext = cipher.encrypt(original_plaintext)

print("--- Base Experiment ---")
print(f"Original Plaintext:  {original_plaintext.hex()}")
print(f"Original Key:        {original_key.hex()} (mysecret)")
print(f"Original Ciphertext: {original_ciphertext.hex()}")
print("=" * 60)

# --- 2. Part 1: Avalanche Effect on Plaintext (Diffusion) ---
print("\n--- Part 1: Avalanche Effect on Plaintext (Diffusion) ---")

# We will store results as a list of dictionaries for Pandas
data_pt = []
for i in range(10):
    # Flip one random bit in the original plaintext
    modified_plaintext, flipped_pos = flip_random_bit(original_plaintext)
    
    # Encrypt with the *same* key
    modified_ciphertext = cipher.encrypt(modified_plaintext)
    
    # Calculate difference
    diff_count = hamming_distance(original_ciphertext, modified_ciphertext)
    
    # Add data to our list
    data_pt.append({
        'Test': f'Test {i+1}',
        'Flipped Bit Pos': flipped_pos,
        'New Ciphertext (hex)': modified_ciphertext.hex(),
        'Bit Difference': diff_count
    })

# Create and print Pandas DataFrame
df_pt = pd.DataFrame(data_pt)
df_pt = df_pt.set_index('Test') # Use 'Test' column as the row index
print(df_pt)
print("-" * 60)

# --- 3. Part 2: Avalanche Effect on Key (Confusion) ---
print("\n--- Part 2: Avalanche Effect on Key (Confusion) ---")

data_key = []
for i in range(10):
    # Flip one random bit in the original key
    modified_key, flipped_pos = flip_random_bit(original_key)
    
    # Create a new cipher object with the *modified* key
    modified_cipher = DES.new(modified_key, DES.MODE_ECB)
    
    # Encrypt the *original* plaintext
    modified_ciphertext = modified_cipher.encrypt(original_plaintext)
    
    # Calculate difference
    diff_count = hamming_distance(original_ciphertext, modified_ciphertext)
    
    # Add data to our list
    data_key.append({
        'Test': f'Test {i+1}',
        'Flipped Bit Pos': flipped_pos,
        'New Ciphertext (hex)': modified_ciphertext.hex(),
        'Bit Difference': diff_count
    })

# Create and print Pandas DataFrame
df_key = pd.DataFrame(data_key)
df_key = df_key.set_index('Test') # Use 'Test' column as the row index
print(df_key)
print("-" * 60)

# --- 4. Part 3: Matplotlib Charting ---
print("\n--- Part 3: Generating Charts ---")

# Create a figure with 2 subplots (one above the other)
# figsize=(10, 12) gives enough space (width, height)
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 12))

# Plot 1: Diffusion (Plaintext Change)
ax1.bar(df_pt.index, df_pt['Bit Difference'], color='blue', label='Bit Diffs')
ax1.set_title('Part 1: Plaintext Bit Change (Diffusion)')
ax1.set_ylabel('Bit Difference (out of 64)')
ax1.set_xlabel('Experiment Run')
ax1.set_ylim(0, 64) # Set Y-axis from 0 to 64
# Add a reference line at 50% (32 bits)
ax1.axhline(y=32, color='red', linestyle='--', label='50% (32 bits)')
ax1.legend()

# Plot 2: Confusion (Key Change)
ax2.bar(df_key.index, df_key['Bit Difference'], color='green', label='Bit Diffs')
ax2.set_title('Part 2: Key Bit Change (Confusion & Parity Bits)')
ax2.set_ylabel('Bit Difference (out of 64)')
ax2.set_xlabel('Experiment Run')
ax2.set_ylim(0, 64) # Set Y-axis from 0 to 64
# Add a reference line at 50% (32 bits)
ax2.axhline(y=32, color='red', linestyle='--', label='50% (32 bits)')
ax2.legend()

# Adjust layout to prevent labels from overlapping
plt.tight_layout()

# Save the combined chart to a file
output_filename = 'des_avalanche_analysis.png'
plt.savefig(output_filename)

print(f"Charts successfully saved to '{output_filename}'")
print("Experiment complete.")
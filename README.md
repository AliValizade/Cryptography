# 🔐 DES Avalanche Effect Analysis

## 🧠 Introduction
This project analyzes the **Avalanche Effect** in the **Data Encryption Standard (DES)** algorithm.  
It demonstrates how **flipping a single bit** in either the **plaintext** or the **key** leads to significant changes in the ciphertext — reflecting the core principles of **diffusion** and **confusion** as defined by Claude Shannon.

---

## ⚙️ Experiment Setup
- **Algorithm:** DES (Data Encryption Standard)  
- **Mode:** ECB (Electronic Codebook)  
- **Key:** `b"mysecret"` (8 bytes)  
- **Plaintext:** `b"\x00\x00\x00\x00\x00\x00\x00\x00"` (8 bytes)  
- **Number of Tests:** 10 random bit flips per experiment  

Two main analyses were conducted:
1. **Diffusion** – flipping a bit in the *plaintext* while keeping the key constant.  
2. **Confusion** – flipping a bit in the *key* while keeping the plaintext constant.  

---

## 📊 Part 1: Avalanche Effect on Plaintext (Diffusion)

| Test | Flipped Bit Position | New Ciphertext (hex) | Bit Difference |
|:----:|:--------------------:|:--------------------:|:--------------:|
| 1 | 19 | 0c9f4d7c435a0dee | 37 |
| 2 | 31 | 5edc8ef2d1b231a2 | 33 |
| 3 | 39 | 87f884ee7f73403e | 35 |
| 4 | 7 | 94da1732d57482d8 | 34 |
| 5 | 59 | ed57d110997f104f | 33 |
| 6 | 11 | e4c17cf4860db0d4 | 30 |
| 7 | 63 | db0b21e37ba449b8 | 38 |
| 8 | 36 | 45e4e98220ab2a6b | 36 |
| 9 | 34 | c0bfe801846fa89a | 33 |
| 10 | 58 | 4db25ab79298649e | 32 |

**Average Bit Difference:** ≈ 34.1 / 64 bits (≈ 53%)  
✅ *Indicates strong diffusion: a single plaintext bit flip affects roughly half the ciphertext bits.*

---

## 🔑 Part 2: Avalanche Effect on Key (Confusion)

| Test | Flipped Bit Position | New Ciphertext (hex) | Bit Difference |
|:----:|:--------------------:|:--------------------:|:--------------:|
| 1 | 29 | 604eac3a49a27576 | 42 |
| 2 | 20 | b950dccbbb668433 | 33 |
| 3 | 33 | 880efcda13155d37 | 36 |
| 4 | 41 | 7eb8f0cb8262d876 | 33 |
| 5 | 36 | 7ec3813c842c1106 | 35 |
| 6 | 1 | addf3a41fc2e26ec | 24 |
| 7 | 0 | fe841e45bc79fead | 0 |
| 8 | 26 | 77a5cef6340009a1 | 29 |
| 9 | 61 | adc7753e24934c0e | 34 |
| 10 | 59 | 15b24af91854268e | 32 |

**Average Bit Difference:** ≈ 29.8 / 64 bits (≈ 46%)  
⚠️ *Confusion effect is slightly weaker here, likely due to DES key parity bits (1 bit per byte not used in encryption).*

---

## 📈 Part 3: Visualization

The results were plotted using `matplotlib`.  
The red dashed line represents the theoretical **50% change threshold (32 bits)** expected for a strong avalanche effect.

![Avalanche Effect Comparison — Plaintext vs Key](des_avalanche_analysis.png)

---

## 🧩 Observations
- **Diffusion (Plaintext change)** achieved near-ideal avalanche results (~50% change).  
- **Confusion (Key change)** was slightly lower, influenced by DES’s **key parity bits** and **56-bit effective key length**.  
- Even minor input changes cause unpredictable, widespread changes in the ciphertext — confirming DES’s non-linearity and strong mixing properties.

---


## 🧪 Running the Experiment

```bash
pip install pycryptodome pandas matplotlib
python des_avalanche_analysis.py
```
‍‍‍
```text
The script will:
- Flip random bits in plaintext and key
- Compute Hamming distances between ciphertexts
- Display data in tabular format
- Generate the comparison chart (des_avalanche_analysis.png)

📚 References
- C. E. Shannon, “Communication Theory of Secrecy Systems,” Bell System Technical Journal, 1949.
- FIPS PUB 46-3, Data Encryption Standard (DES), National Institute of Standards and Technology.

Author: Ali Valizadeh  
Course / Project: Applied Cryptography — DES Avalanche Analysis  
Language: Python 3  
Libraries: pycryptodome, pandas, matplotlib
```




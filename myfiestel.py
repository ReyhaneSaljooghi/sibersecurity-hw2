import itertools
S_BOX = [
    [14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7],
    [0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8],
    [4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0],
    [15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13]
]

def generate_subkeys(main_key):
    subkeys = []
    key_bits = list(map(int, list(main_key)))
    for i in range(12):
        if i % 2 == 0:
            key_bits = key_bits[3:] + key_bits[:3]
        else:
            key_bits = key_bits[2:] + key_bits[:2]

        #  S-box
        row = int(f"{key_bits[0]}{key_bits[47]}", 2)
        col = int(''.join(map(str, key_bits[1:5])), 2)
        subkey = format(S_BOX[row][col], '032b')
        subkeys.append(list(map(int, list(subkey))))

    return subkeys


# Round function F
def feistel_function(R, K):

    table = [R[i * 4:((i + 1) * 4 )] for i in range(8)]

    new_table1 = [
        [table[0][j] ^ table[2][j] for j in range(4)],
        [table[1][j] ^ table[3][j] for j in range(4)],
        [table[4][j] ^ table[6][j] for j in range(4)],
        [table[5][j] ^ table[7][j] for j in range(4)]
    ]

    new_table2 = [
        [table[0][j] ^ table[7][j] for j in range(4)],
        [table[1][j] ^ table[6][j] for j in range(4)],
        [table[2][j] ^ table[5][j] for j in range(4)],
        [table[3][j] ^ table[4][j] for j in range(4)]
    ]
    final_result = list(itertools.chain.from_iterable(new_table1 + new_table2))
    return [final_result[i] ^ K[i] for i in range(32)]


# Feistel encryption
def encrypt(plaintext, main_key):
    plaintext_bits = list(map(int, list(plaintext)))
    L, R = plaintext_bits[:32], plaintext_bits[32:]
    subkeys = generate_subkeys(main_key)

    for i in range(12):
        L, R = R, [l ^ f for l, f in zip(L, feistel_function(R, subkeys[i]))]

    combined_bits = L + R
    ciphertext = ''.join(map(str, combined_bits))
    return ciphertext

def decrypt(ciphertext, main_key):
    ciphertext_bits = list(map(int, list(ciphertext)))
    L, R = ciphertext_bits[:32], ciphertext_bits[32:]
    subkeys = generate_subkeys(main_key)[::-1]

    for i in range(12):
        R, L = L, [l ^ f for l, f in zip(R, feistel_function(L, subkeys[i]))]

    combined_bits = L + R
    plaintext = ''.join(map(str, combined_bits))
    return plaintext


plaintext = "0100111000101101011010000110010101110011011010000001110001101001"  # 64
key = "011000100110010101101000011001010111001101101000"  # 48
ciphertext = encrypt(plaintext, key)
print(f"Ciphertext: {ciphertext}")
plainrtext2 = decrypt(ciphertext,key)
print(f"plaintext: {plainrtext2}")

# D5 multiplication table for Verhoeff algorithm
_D5 = [
    [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
    [1, 2, 3, 4, 0, 6, 7, 8, 9, 5],
    [2, 3, 4, 0, 1, 7, 8, 9, 5, 6],
    [3, 4, 0, 1, 2, 8, 9, 5, 6, 7],
    [4, 0, 1, 2, 3, 9, 5, 6, 7, 8],
    [5, 9, 8, 7, 6, 0, 4, 3, 2, 1],
    [6, 5, 9, 8, 7, 1, 0, 4, 3, 2],
    [7, 6, 5, 9, 8, 2, 1, 0, 4, 3],
    [8, 7, 6, 5, 9, 3, 2, 1, 0, 4],
    [9, 8, 7, 6, 5, 4, 3, 2, 1, 0],
]

# Permutation table for Verhoeff algorithm
_P = [
    [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
    [1, 5, 7, 6, 2, 8, 3, 0, 9, 4],
    [5, 8, 0, 3, 7, 9, 6, 1, 4, 2],
    [8, 9, 1, 6, 0, 4, 3, 5, 2, 7],
    [9, 4, 5, 3, 1, 2, 6, 8, 7, 0],
    [4, 2, 8, 6, 5, 7, 3, 9, 0, 1],
    [2, 7, 9, 3, 8, 0, 6, 4, 1, 5],
    [7, 0, 4, 6, 9, 1, 3, 2, 5, 8],
]

def luhn_ok(digits: str) -> bool:
    """
    Validates a credit or debit card number string using the Luhn checksum algorithm (Mod 10).
    Requires between 13 and 19 numeric digits.
    """
    clean_digits = [int(c) for c in str(digits) if c.isdigit()]
    if len(clean_digits) < 13 or len(clean_digits) > 19:
        return False

    checksum = 0
    reverse_digits = clean_digits[::-1]

    for idx, num in enumerate(reverse_digits):
        if idx % 2 == 1:
            doubled = num * 2
            checksum += doubled - 9 if doubled > 9 else doubled
        else:
            checksum += num

    return checksum % 10 == 0

def verhoeff_ok(digits: str) -> bool:
    """
    Validates a number string (such as an Indian Aadhaar number) using the Verhoeff checksum algorithm.
    Indian Aadhaar requires exactly 12 digits starting with 2-9.
    """
    clean_digits = [int(c) for c in str(digits) if c.isdigit()]
    if len(clean_digits) != 12:
        return False

    # First digit of 12-digit Aadhaar cannot be 0 or 1
    if clean_digits[0] < 2:
        return False

    checksum = 0
    for idx, digit in enumerate(reversed(clean_digits)):
        checksum = _D5[checksum][_P[idx % 8][digit]]

    return checksum == 0

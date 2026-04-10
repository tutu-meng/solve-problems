import sys

def is_heptaphobic(n):
    s = str(n)
    if n % 7 == 0:
        return False
    digits = [int(d) for d in s]
    L = len(digits)
    for i in range(L):
        for j in range(i + 1, L):
            # Try swapping digits[i] and digits[j]
            d_i, d_j = digits[i], digits[j]
            if i == 0 and d_j == 0:
                continue
            # Note: leading zero before swap is not possible for positive int n
            # Swapping i, j
            new_digits = list(digits)
            new_digits[i], new_digits[j] = d_j, d_i
            # The resulting number
            val = 0
            for d in new_digits:
                val = val * 10 + d
            if val % 7 == 0:
                return False
    return True

def count_brute(N):
    cnt = 0
    for i in range(1, N):
        if is_heptaphobic(i):
            cnt += 1
    return cnt

if __name__ == "__main__":
    print(f"C(100) = {count_brute(100)}")
    print(f"C(1000) = {count_brute(1000)}")

def is_palindrome(n):
    s = str(n)
    return s == s[::-1]

def is_lychrel(n):
    current = n
    for _ in range(50):
        current = current + int(str(current)[::-1])
        if is_palindrome(current):
            return False
    return True

def solve():
    count = 0
    for i in range(1, 10000):
        if is_lychrel(i):
            count += 1
    return count

if __name__ == "__main__":
    result = solve()
    print(result)

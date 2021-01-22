def triangle(x, y):
    for i in range(x, y + 1):
        yield i * (i + 1) // 2

def main():
    for i in triangle(1, 5):
        print(i)

if __name__ == "__main__":
    main()
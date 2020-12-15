def main():
    while True:
        word = input("Word: ")
        if word == "":
            break
        for i in range(len(word)):
            if i == 0:
                print(word)
            elif i == len(word) - 1:
                for k in range(len(word)):
                    print(word[-k - 1], end="")
                print()
            else:
                print(word[i], end="")
                for j in range(len(word) - 2):
                    print(" ", end="")
                print(word[-i - 1])

if __name__ == "__main__":
    main()

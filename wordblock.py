def main():
    while True:
        word = input("Word: ")
        if word == "":
            break
        for i in range(len(word)):
            print(word[i:len(word)], end="")
            print(word[0:i])

if __name__ == "__main__":
    main()

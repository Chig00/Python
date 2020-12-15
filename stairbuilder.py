#!/usr/bin/env python3

"""Stair builder.

This script accepts input from the user and
creates a staircase of the size given.

For example, if 3 is the input:
  X
 XX
XXX will be printed.
"""

# If the size of the staircase is equal to this
# constant, the main() function returns.
QUIT = 0
STAIR = "X"

def build(size):
    """Print a staircase of the given size."""
    for i in range(1, size + 1):
        space = " " * (size - i)
        stair = STAIR * i
        print(space + stair)

def main():
    """Get input and print the staircase."""
    while True:
        try:
            size = int(input("Size: "))
            if size == QUIT:
                return
            elif size < 1:
                raise ValueError
        except ValueError:
            print("Please use an integer greater than 0.")
        else:
            build(size)

if __name__ == "__main__":
    main()

""" All binary bit functions expressed in terms of NAND."""

# Negated Conjunction
nand = lambda x, y: not (x and y)

# 1st Identity
id1 = lambda x, y: x

# 2nd Identity
id2 = lambda x, y: y

# 1st Negation
neg1 = lambda x, y: nand(x, x)

# 2nd Negation
neg2 = lambda x, y: nand(y, y)

# Tautology
top = lambda x, y: nand(nand(x, x), x)

# Contradiction
bottom = lambda x, y: nand(nand(nand(x, x), x), nand(nand(y, y), y))

# Conjuction
con = lambda x, y: nand(nand(x, y), nand(x, y))

# Disjunction
dis = lambda x, y: nand(nand(x, x), nand(y, y))

# Implication
imp = lambda x, y: nand(nand(nand(x, x), nand(x, x)), nand(y, y))

# Reverse Implication
rmp = lambda x, y: nand(nand(x, x), nand(nand(y, y), nand(y, y)))

# Negated Disjunction
nor = lambda x, y: nand(nand(nand(x, x), nand(y, y)), nand(nand(x, x), nand(y, y)))

# Negated Implication
nimp = lambda x, y: nand(
    nand(nand(nand(x, x), nand(x, x)), nand(y, y)),
    nand(nand(nand(x, x), nand(x, x)), nand(y, y))
)

# Negated Reverse Implication
nrmp = lambda x, y: nand(
    nand(nand(x, x), nand(nand(y, y), nand(y, y))),
    nand(nand(x, x),nand(nand(y, y), nand(y, y)))
)

# Exclusive Disjunction
xor = lambda x, y: nand(
    nand(nand(x, y), nand(nand(x, x), nand(y, y))),
    nand(nand(x, y), nand(nand(x, x), nand(y, y)))
)

# Negated Exclusive Disjunction
xnor = lambda x, y: nand(
    nand(nand(nand(x, y), nand(x, y)), nand(nand(x, y), nand(x, y))),
    nand(
        nand(nand(nand(x, x), nand(y, y)), nand(nand(x, x), nand(y, y))),
        nand(nand(nand(x, x), nand(y, y)), nand(nand(x, x), nand(y, y)))
    )
)

# All functions in ascending order.
FUNCTIONS = [
    bottom, con, nimp, id1,
    nrmp, id2, xor, dis,
    nor, xnor, neg2, rmp,
    neg1, imp, nand, top
]

def main():
    """Displays all of the functions' values of all valuations."""
    
    for x in (False, True):
        for y in (False, True):
            for i in (int(f(x, y)) for f in FUNCTIONS):
                print(i, end = ' ')
            
            print()

if __name__ == "__main__":
    main()
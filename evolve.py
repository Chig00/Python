import time # Used for getting the current time for seeding.
import random # Used for producing random numbers.

ATTRIBUTES = 5 # The number of atrributes for an organism.
MIN = 0 # The minimum value of an organism's attribute.
MAX = 5 # The maximum value of an organism's attribute.
GENERATION = 5 # The number of organisms in each generation.
GENERATIONS = 10 # The number of generations to evolve.
ORGANISM_MAX = ATTRIBUTES * MAX # The maximum organism value.
GENERATION_MAX = ORGANISM_MAX * GENERATION # The maximum generation value.
FATHER_CHANCE = 0.45 # The probability of inheriting an attribute from the father.
MOTHER_CHANCE = 0.45 # The probability of inheriting an attribute from the mother.

class Organism:
    """An organism with values for its attributes and the ability to reproduce."""
    
    def __init__(self, father = None, mother = None):
        """Constructs an organism with random or inherited attributes."""
        
        self.stats = []
        
        # Attributes are inherited from the parents.
        if (father and mother):
            for i in range(ATTRIBUTES):
                choice = random.random()
            
                # Attribute inherited from the father.
                if choice < FATHER_CHANCE:
                    self.stats.append(father.stats[i])
                
                # Attribute inherited from the mother.
                elif choice < FATHER_CHANCE + MOTHER_CHANCE:
                    self.stats.append(mother.stats[i])
                
                # Attribute randomly generated.
                else:
                    self.stats.append(random.randint(MIN, MAX))
        
        # Attributes are randomly generated.
        else:
            for i in range(ATTRIBUTES):
                self.stats.append(random.randint(MIN, MAX))
    
    def value(self):
        """The value of the organism is the sum of its attribute values."""
        
        return sum(self.stats)

class Generation:
    """A generation contains organisms: the best of which will produce the next generation."""

    def __init__(self):
        """The first generation is filled with random organisms."""
        
        self.organisms = []
        
        for i in range(GENERATION):
            self.organisms.append(Organism())

        # The organisms are sorted by their value.
        self.sort()
    
    def __repr__(self):
        """Returns information about the generation."""
        
        return str(100 * self.value() / GENERATION_MAX) + '%'
    
    def value(self):
        """ Returns the total value of the generation."""
        
        return sum([o.value() for o in self.organisms])
    
    def evolve(self):
        """Uses the two best organisms in the generation to produce the next generation."""
        
        generation = []
        
        for i in range(GENERATION):
            generation.append(
                Organism(self.organisms[0], self.organisms[1])
            )
        
        self.organisms = generation
        self.sort()
    
    def sort(self):
        """Sorts the organisms by value (descending)."""
        
        self.organisms.sort(key = (lambda o: o.value()), reverse = True)

def main():
    """Seeds the RNG, creates an initial generation, and evolves the population."""
    
    random.seed(time.time()) # The RNG is seeded with the time.
    population = Generation() # The current population is randomly generated.
    
    for i in range(GENERATIONS):
        population.evolve() # The population evolves to the next generation.
    
    print(population) # The population's statistics are displayed.

# Not run when imported.
if __name__ == "__main__":
    main()
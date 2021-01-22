class Integer:
    def __init__(self, value = 0):
        self.value = value
    
    def __add__(self, other):
        return Integer(self.value + other.value)
    
    def __repr__(self):
        return str(self.value)
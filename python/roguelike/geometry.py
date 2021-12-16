import math

class DOT:

    def __init__(self, x, y):
        self.pos = [x, y]

class VECTOR:

    def __init__(self, x, y):
        self.pos = [x, y]

    @property
    def lenght(self):
        return (self.pos[0]**2+self.pos[1]**2)**(1/2)

    def normalise(self):
        self.pos = [i/self.lenght for i in self.pos]

    def __mul__(self, other):
        if type(other) in [float, int]:
            return VECTOR(*[i*other for i in self.pos])

    def __rmul__(self, other):
        return self*other

    def __add__(self, other):
        return VECTOR(*[self.pos[i]+other.pos[i] for i in range(2)])

    def __radd__(self, other):
        return self+other

    def __neg__(self):
        return VECTOR(*[-i for i in self.pos])

    def __sub__(self, other):
        return self+(-other)

    def __rsub__(self, other):
        return self-other

    def __getitem__(self, key):
        return self.pos[key]

    def __len__(self):
        return 2

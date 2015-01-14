"""Represents a two-dimensional vector. 

This is an utility class for representation of points and vectors in an
two-dimensional coordinate space. It provides methods for useful
mathematical operations (add, sub, mul, div, etc.) with other vectors
and scalars.
"""

import math

class Vec2:

    def __init__(self, x = (0, 0), y = None):
        if y == None:
            self.x = x[0]
            self.y = x[1]
        else:
            self.x = x
            self.y = y

    def __repr__(self):
        return 'Vec2(%s, %s)' % (self.x, self.y)

    def __len__(self):
        return 2

    def __getitem__(self, key):
        if key == 0:
            return self.x
        elif key == 1:
            return self.y
        else:
            raise IndexError("index out of range")            

    def __setitem__(self, key, value):
        if key == 0:
            self.x = value
        elif key == 1:
            self.y = value
        else:
            raise IndexError("index out of range")

    def __add__(self, other):
        if isinstance(other, Vec2):
            return Vec2((self.x + other.x, self.y + other.y))
        elif hasattr(other, '__getitem__'):
            return Vec2((self.x + other[0], self.y + other[1]))            
        else:
            return Vec2((self.x + other, self.y + other))

    __radd__ = __add__

    def __iadd__(self, other):
        if isinstance(other, Vec2):
            self.x += other.x
            self.y += other.y
        elif hasattr(other, "__getitem__"):
            self.x += other[0]
            self.y += other[1]
        else:
            self.x += other
            self.y += other
        return self

    def __sub__(self, other):
        if isinstance(other, Vec2):
            return Vec2((self.x - other.x, self.y - other.y))
        elif hasattr(other, '__getitem__'):
            return Vec2((self.x - other[0], self.y - other[1]))            
        else:
            return Vec2((self.x - other, self.y - other))
    
    def __rsub__(self, other):
        if isinstance(other, Vec2):
            return Vec2((other.x - self.x, other.y - self.y))
        elif hasattr(other, '__getitem__'):
            return Vec2((other[0] - self.x, other[1] - self.y))            
        else:
            return Vec2((other - self.x, other - self.y))

    def __isub__(self, other):
        if isinstance(other, Vec2):
            self.x -= other.x
            self.y -= other.y
        elif hasattr(other, "__getitem__"):
            self.x -= other[0]
            self.y -= other[1]
        else:
            self.x -= other
            self.y -= other
        return self

    def __mul__(self, other):
        if isinstance(other, Vec2):
            return Vec2((self.x * other.x, self.y * other.y))
        elif hasattr(other, '__getitem__'):
            return Vec2((self.x * other[0], self.y * other[1]))            
        else:
            return Vec2((self.x * other, self.y * other))

    __rmul__ = __mul__

    def __imul__(self, other):
        if isinstance(other, Vec2):
            self.x *= other.x
            self.y *= other.y
        elif hasattr(other, '__getitem__'):
            self.x *= other[0]
            self.y *= other[1]
        else:
            self.x *= other
            self.y *= other
        return self

    def set_to(self, other):
        if isinstance(other, Vec2):
            self.x = other.x
            self.y = other.y
        elif hasattr(other, '__getitem__'):
            self.x = other[0]
            self.y = other[1]
        else:
            self.x = other
            self.y = other

    def length_squared(self):
        """Returns the squared length of this vector."""
        return self.x * self.x + self.y * self.y

    def length(self):
        """Returns the length of this vector."""
        return math.sqrt(self.x * self.x + self.y * self.y)

    def rotate(self, phi):
        """Rotates this vector in-place by the given angle in radians."""
        cos_phi = math.cos(phi)
        sin_phi = math.sin(phi)
        
        x = cos_phi * self.x - sin_phi * self.y
        self.y = sin_phi * self.x + cos_phi * self.y
        self.x = x

    def rotated(self, phi):
        """Rotates this vector by the given angle in radians.
        This method returns a new vector object and doesn not motify
        this object.
        """
        cos_phi = math.cos(phi)
        sin_phi = math.sin(phi)

        return Vec2((cos_phi * self.x - sin_phi * self.y,
                    sin_phi * self.x + cos_phi * self.y))
    
    def normalized(self):
        """Normalizes this vector.
        This method returns a new vector object and does not motify
        this object.
        """
        l = self.length()
        return Vec2(self.x / l, self.y / l)

    def normalize(self):
        """Normalizes this vector in-place."""
        l = self.length()
        self.x /= l
        self.y /= l

    def dot(self, other):
        """Returns the dot product for this and the given vector."""
        return self.x * other.x + self.y * other.y

    def perpendicularize(self):
        """Returns a vector that is perpendicular to this vector."""
        x = self.x
        self.x = self.y
        self.y = -x
        
    def perpendicularized(self):
        """Converts this vector to be perpendicular to itself."""
        return Vec2(self.y, -self.x)        
        

from math import sqrt
from decimal import Decimal, getcontext

getcontext().prec = 30


class Vector(object):

    CANNOT_NORMALIZE_ZERO_VECTOR_MSG = "Cannot normalize the zero vector"

    def __init__(self, coordinates):
        """Convert co-ordinate list to a tuple of decimal co-ordinates."""
        try:
            if not coordinates:
                raise ValueError
            self.coordinates = tuple([Decimal(x) for x in coordinates])
            self.dimension = len(coordinates)

        except ValueError:
            raise ValueError('The coordinates must be non-empty')

        except TypeError:
            raise TypeError('The coordinates must be an iterable')

    def __str__(self):
        return 'Vector: {}'.format(self.coordinates)

    def __eq__(self, v):
        return self.coordinates == v.coordinates

    def scale(self, c):
        """Scale a vector by the given constant."""
        new_coordinates = [Decimal(c) * x for x in self.coordinates]
        return Vector(new_coordinates)

    def magnitude(self):
        """
        Find the magnitude of a vector.

        |Vector (x, y, z)| = sqrt(x ^ 2 + y ^ 2 + z ^ 2)
        """
        vector_list = [x ** 2 for x in self.coordinates]
        vector_magnitude = sqrt(sum(vector_list))
        return Decimal(vector_magnitude)

    def normalize(self):
        """
        Convert given vector to its unit vector in the same direction.

        Unit Vector A = (Vector A / |Vector A|)
        """
        try:
            vector_magnitude = self.magnitude()
            return self.scale(Decimal('1.0') / vector_magnitude)
        except ZeroDivisionError:
            raise Exception(self.CANNOT_NORMALIZE_ZERO_VECTOR_MSG)


magnitude_vector_1 = Vector([-0.221, 7.437])
print magnitude_vector_1.magnitude()
magnitude_vector_2 = Vector([8.813, -1.331, -6.247])
print magnitude_vector_2.magnitude()

normalize_vector_1 = Vector([5.581, -2.136])
print normalize_vector_1.normalize()
normalize_vector_2 = Vector([1.996, 3.108, -4.554])
print normalize_vector_2.normalize()

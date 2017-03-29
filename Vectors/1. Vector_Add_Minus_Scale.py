from decimal import Decimal, getcontext

getcontext().prec = 30


class Vector(object):
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

    def add(self, v):
        """Add two vectors to find resultant vector."""
        new_coordinates = [x + y for x,
                           y in zip(self.coordinates, v.coordinates)]
        return Vector(new_coordinates)

    def minus(self, v):
        """Subtract two vectors to find the difference vector."""
        new_coordinates = [x - y for x,
                           y in zip(self.coordinates, v.coordinates)]
        return Vector(new_coordinates)

    def scale(self, c):
        """Scale a vector by the given constant."""
        new_coordinates = [Decimal(c) * x for x in self.coordinates]
        return Vector(new_coordinates)


add_vector_1 = Vector([8.218, -9.341])
add_vector_2 = Vector([-1.129, 2.111])
print add_vector_1.add(add_vector_2)

minus_vector_1 = Vector([7.119, 8.215])
minus_vector_2 = Vector([-8.223, 0.878])
print minus_vector_1.minus(minus_vector_2)

scale_vector = Vector([1.671, -1.012, -0.318])
scale_factor = 7.41
print scale_vector.scale(scale_factor)

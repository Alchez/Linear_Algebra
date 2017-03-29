from math import sqrt, acos, degrees
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

    def dot_product(self, v):
        """
        Find the dot (inner) product of two vectors.

        Vector A • Vector B = |A| * |B| * cos (angle)

        Simplified: Vector A • Vector B = (A[0]*B[0]) + (A[1]*B[1]) + ...
        """
        dot_product_value = [x * y for x,
                             y in zip(self.coordinates, v.coordinates)]
        return round(sum(dot_product_value), 3)

    def get_degree(self, v, in_degrees=False):
        """
        Find the smaller angle between two vectors.

        Angle between Vectors A and B = acos((Vector A • Vector B) / |A| * |B|)

        Simplified: Angle = acos(Unit Vector A • Unit Vector B)
        """
        try:
            normalize_x = self.normalize()
            normalize_y = v.normalize()
            degree_in_radians = acos(normalize_x.dot_product(normalize_y))

            if in_degrees:
                return degrees(degree_in_radians)
            else:
                return degree_in_radians

        except Exception as e:
            if str(e) == self.CANNOT_NORMALIZE_ZERO_VECTOR_MSG:
                raise Exception("Cannot compute an angle with a zero vector")
            else:
                raise e


dot_vector_1_a = Vector([7.887, 4.138])
dot_vector_1_b = Vector([-8.802, 6.776])
print dot_vector_1_a.dot_product(dot_vector_1_b)
dot_vector_2_a = Vector([-5.955, -4.904, -1.874])
dot_vector_2_b = Vector([-4.496, -8.755, 7.103])
print dot_vector_2_a.dot_product(dot_vector_2_b)

get_degree_1_a = Vector([3.183, -7.627])
get_degree_1_b = Vector([-2.668, 5.319])
print get_degree_1_a.get_degree(get_degree_1_b)
get_degree_2_a = Vector([7.35, 0.221, 5.188])
get_degree_2_b = Vector([2.751, 8.259, 3.985])
print get_degree_2_a.get_degree(get_degree_2_b, True)

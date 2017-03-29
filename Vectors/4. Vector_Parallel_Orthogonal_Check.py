from math import sqrt, acos, degrees, pi
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

    def is_orthogonal(self, v, tolerance=1e-10):
        """
        Check if two vectors are perpendicular to each other.

        If Vector A • Vector B = 0, A and B are orthogonal.
        """
        return abs(self.dot_product(v)) < tolerance

    def is_parallel(self, v):
        """
        Check if two vectors are parallel to each other.

        If Vector A = Constant * Vector B in the same (or opposite) direction,
        A and B are parallel.
        """
        return (self.is_zero() or
                v.is_zero() or
                self.get_degree(v) == 0 or
                self.get_degree(v) == pi)

    def is_zero(self, tolerance=1e-10):
        """Check if a vector is a zero vector."""
        return self.magnitude() < tolerance

    def check_vector(self, v):
        """Performs parallel and orthogonal checks on two vectors."""
        p_true = self.is_parallel(v)
        o_true = self.is_orthogonal(v)

        if p_true and o_true:
            return "both parallel and orthogonal!"
        elif p_true:
            return "parallel!"
        elif o_true:
            return "orthogonal!"
        else:
            return "neither parallel nor orthogonal..."


print "First pair is..."
parallel_or_orthogonal_1_a = Vector([-7.579, -7.88])
parallel_or_orthogonal_1_b = Vector([22.737, 23.64])
print parallel_or_orthogonal_1_a.check_vector(parallel_or_orthogonal_1_b)
print "Second pair is..."
parallel_or_orthogonal_2_a = Vector([-2.029, 9.97, 4.172])
parallel_or_orthogonal_2_b = Vector([-9.231, -6.639, -7.245])
print parallel_or_orthogonal_2_a.check_vector(parallel_or_orthogonal_2_b)
print "Third pair is..."
parallel_or_orthogonal_3_a = Vector([-2.328, -7.284, -1.214])
parallel_or_orthogonal_3_b = Vector([-1.821, 1.072, -2.94])
print parallel_or_orthogonal_3_a.check_vector(parallel_or_orthogonal_3_b)
print "Fourth pair is..."
parallel_or_orthogonal_4_a = Vector([2.118, 4.827])
parallel_or_orthogonal_4_b = Vector([0, 0])
print parallel_or_orthogonal_4_a.check_vector(parallel_or_orthogonal_4_b)

from math import sqrt, acos, degrees
from decimal import Decimal, getcontext

getcontext().prec = 30


class Vector(object):

    CANNOT_NORMALIZE_ZERO_VECTOR_MSG = "Cannot normalize the zero vector"
    NO_UNIQUE_PARALLEL_COMPONENT_MSG = "No unique parallel component exists!"
    NO_UNIQUE_ORTHOGONAL_COMPONENT_MSG = "No unique orthogonal component exists!"

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

    def minus(self, v):
        """Subtract two vectors to find the difference vector."""
        new_coordinates = [x - y for x,
                           y in zip(self.coordinates, v.coordinates)]
        return Vector(new_coordinates)

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

    def parallel_projection(self, basis):
        """
        Find the projection of given vector on basis vector.

        |Projection of Vector A on Vector B| = |Vector A| * cos(angle between A and B)

        Simplified: Projection of A on B = (Vector A • Unit Vector B) * Unit Vector B
        """
        try:
            unit_vector = basis.normalize()
            scalar_coefficient = self.dot_product(unit_vector)
            return unit_vector.scale(scalar_coefficient)

        except Exception as e:
            if str(e) == self.CANNOT_NORMALIZE_ZERO_VECTOR_MSG:
                raise Exception(self.NO_UNIQUE_PARALLEL_COMPONENT_MSG)
            else:
                raise e

    def orthogonal_projection(self, basis):
        """
        Find the projection of given vector perpendicular to basis vector.

        Perpendicular projection of A to B = Vector A - Parallel projection of A on B
        """
        try:
            parallel_vector = self.parallel_projection(basis)
            return self.minus(parallel_vector)

        except Exception as e:
            if str(e) == self.CANNOT_NORMALIZE_ZERO_VECTOR_MSG:
                raise Exception(self.NO_UNIQUE_ORTHOGONAL_COMPONENT_MSG)
            else:
                raise e

    def component_vectors(self, basis):
        """Find the parallel and orthogonal projections of a vector with respect to a basis vector."""
        parallel_projection = self.parallel_projection(basis)
        orthogonal_projection = self.orthogonal_projection(basis)
        return parallel_projection, orthogonal_projection


parallel_proj_v = Vector([3.039, 1.879])
parallel_proj_b = Vector([0.825, 2.036])
print parallel_proj_v.parallel_projection(parallel_proj_b)
orthogonal_projection_v = Vector([-9.88, -3.264, -8.159])
orthogonal_projection_b = Vector([-2.155, -9.353, -9.473])
print orthogonal_projection_v.orthogonal_projection(orthogonal_projection_b)
component_vectors_v = Vector([3.009, -6.172, 3.692, -2.51])
component_vectors_b = Vector([6.404, -9.144, 2.759, 8.718])
component_parallel, component_orthogonal = component_vectors_v.component_vectors(
    component_vectors_b)
print component_parallel, "\n", component_orthogonal

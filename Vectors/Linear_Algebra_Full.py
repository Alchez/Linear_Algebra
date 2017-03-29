from math import sqrt, acos, degrees, pi
from decimal import Decimal, getcontext

getcontext().prec = 30


class Vector(object):

    CANNOT_NORMALIZE_ZERO_VECTOR_MSG = "Cannot normalize the zero vector"
    NO_UNIQUE_PARALLEL_COMPONENT_MSG = "No unique parallel component exists!"
    NO_UNIQUE_ORTHOGONAL_COMPONENT_MSG = "No unique orthogonal component exists!"
    ONLY_DEFINED_IN_TWO_THREE_DIMS_MSG = "Cross-product only applicable to 2D or 3D vectors"

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

    def cross_product(self, v):
        """
        Find the cross-product of two (2D or 3D) vectors.

        |Vector A x Vector B| = |Vector A| * |Vector B| * sin (angle)

        Simplified: Vector A x Vector B = [    y1 * z2 -  y2 * z1,
                                            - (x1 * z2 - x2 * z1),
                                               x1 * y2 - x2 * y1 ]
        """
        try:
            x_1, y_1, z_1 = self.coordinates
            x_2, y_2, z_2 = v.coordinates
            new_coordinates = [y_1 * z_2 - y_2 * z_1,
                               - (x_1 * z_2 - x_2 * z_1),
                               x_1 * y_2 - x_2 * y_1]
            return Vector(new_coordinates)

        except ValueError as e:
            msg = str(e)
            if msg == "need more than 2 values to unpack":
                self_in_3D = Vector(self.coordinates + ('0',))
                v_in_3D = Vector(self.coordinates + ('0',))
                return self_in_3D.cross_product(v_in_3D)
            elif (msg == 'too many values to unpack' or
                  'need more than 1 value to unpack'):
                raise Exception(self.ONLY_DEFINED_IN_TWO_THREE_DIMS_MSG)
            else:
                raise e

    def parallelogram_area(self, v):
        """
        Find the area of parallelogram formed by two vectors.

        Area = |Vector A x Vector B|
        """
        cross_product = self.cross_product(v)
        return cross_product.magnitude()

    def triangle_area(self, v):
        """
        Find the area of triangle formed by two vectors.

        Area = 0.5 * |Vector A x Vector B|
        """
        return self.parallelogram_area(v) / Decimal('2.0')


# Start of example cases
add_vector_1 = Vector([8.218, -9.341])
add_vector_2 = Vector([-1.129, 2.111])
print add_vector_1.add(add_vector_2)

minus_vector_1 = Vector([7.119, 8.215])
minus_vector_2 = Vector([-8.223, 0.878])
print minus_vector_1.minus(minus_vector_2)

scale_vector = Vector([1.671, -1.012, -0.318])
scale_factor = 7.41
print scale_vector.scale(scale_factor)

magnitude_vector_1 = Vector([-0.221, 7.437])
print magnitude_vector_1.magnitude()
magnitude_vector_2 = Vector([8.813, -1.331, -6.247])
print magnitude_vector_2.magnitude()

normalize_vector_1 = Vector([5.581, -2.136])
print normalize_vector_1.normalize()
normalize_vector_2 = Vector([1.996, 3.108, -4.554])
print normalize_vector_2.normalize()

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

cross_vector_1_v = Vector([8.462, 7.893, -8.187])
cross_vector_1_w = Vector([6.984, -5.975, 4.778])
print cross_vector_1_v.cross_product(cross_vector_1_w)
cross_vector_2_v = Vector([-8.987, -9.838, 5.031])
cross_vector_2_w = Vector([-4.268, -1.861, -8.866])
print cross_vector_2_v.parallelogram_area(cross_vector_2_w)
cross_vector_3_v = Vector([1.5, 9.547, 3.691])
cross_vector_3_w = Vector([-6.007, 0.124, 5.772])
print cross_vector_3_v.triangle_area(cross_vector_3_w)

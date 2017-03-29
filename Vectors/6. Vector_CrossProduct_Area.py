from math import sqrt
from decimal import Decimal, getcontext

getcontext().prec = 30


class Vector(object):

    CANNOT_NORMALIZE_ZERO_VECTOR_MSG = "Cannot normalize the zero vector"
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

    def magnitude(self):
        """
        Find the magnitude of a vector.

        |Vector (x, y, z)| = sqrt(x ^ 2 + y ^ 2 + z ^ 2)
        """
        vector_list = [x ** 2 for x in self.coordinates]
        vector_magnitude = sqrt(sum(vector_list))
        return Decimal(vector_magnitude)

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


cross_vector_1_v = Vector([8.462, 7.893, -8.187])
cross_vector_1_w = Vector([6.984, -5.975, 4.778])
print cross_vector_1_v.cross_product(cross_vector_1_w)
cross_vector_2_v = Vector([-8.987, -9.838, 5.031])
cross_vector_2_w = Vector([-4.268, -1.861, -8.866])
print cross_vector_2_v.parallelogram_area(cross_vector_2_w)
cross_vector_3_v = Vector([1.5, 9.547, 3.691])
cross_vector_3_w = Vector([-6.007, 0.124, 5.772])
print cross_vector_3_v.triangle_area(cross_vector_3_w)

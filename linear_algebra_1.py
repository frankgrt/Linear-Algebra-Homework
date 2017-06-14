from math import sqrt, acos , pi
from decimal import Decimal, getcontext

getcontext().prec = 30

class Vector(object):

    CANNOT_NORMALIZE_ZERO_VECTOR_MSG = 'Cannot normalize the zero vector'
    def __init__(self, coordinates):
        try:
            if not coordinates:
                raise ValueError
            self.coordinates = tuple([Decimal(x) for x in coordinates])
            self.dimension = len(coordinates)

        except ValueError:
            raise ValueError('The coordinates must be nonempty')

        except TypeError:
            raise TypeError('The coordinates must be an iterable')


    def __str__(self):
        return 'Vector: {}'.format(self.coordinates)


    def __eq__(self, v):
        return self.coordinates == v.coordinates

    def plus(self, v):
        new_coordinates = [x+y for x,y in zip(self.coordinates, v.coordinates)]
        return Vector(new_coordinates)

    def minus(self, v):
        new_coordinates = [x-y for x,y in zip(self.coordinates, v.coordinates)]
        return Vector(new_coordinates)

    def times_scalar(self, c):
        new_coordinates = [Decimal(c)*x for x in self.coordinates]
        return Vector(new_coordinates)

    def magnitude(self):
        coordinates_squared = [x**Decimal(2) for x in self.coordinates]
        return sum(coordinates_squared)**Decimal(0.5)

    def normalized(self):
        try:
            magnitude = self.magnitude()
            return self.times_scalar(Decimal('1.0')/Decimal(magnitude))

        except ZeroDivisionError:
            raise Exception('Can not normalize the zero vector')

    def dot_product(self,v):
        return sum([x*y for x,y in zip(self.coordinates,v.coordinates)])

    def angle_with(self,v,in_degree = False):
        try:
            u1 = self.normalized()
            u2 = v.normalized()
            angle_in_radians = acos(u1.dot_product(u2))

            if in_degree:
                degrees_per_radian = 180. / pi
                return angle_in_radians * degrees_per_radian
            else:
                return angle_in_radians
        except Exception as e:
            if str(e) == self.CANNOT_NORMALIZE_ZERO_VECTOR_MSG:
                raise Exception('Cannot compute an angle with the zero vector')
            else:
                raise e

    def check_parallel(self,v,tolerance=1e-5):
        return abs(abs(self.dot_product(v)) - self.magnitude() * v.magnitude()) < tolerance

    def check_orthogonal(self,v,tolerance=1e-10):
        return abs(self.dot_product(v)) < tolerance

vector_1 = Vector([-7.579,-7.88])
vector_2 = Vector([22.737,23.64])
print vector_1.check_parallel(vector_2)
print vector_1.check_orthogonal(vector_2)

vector_1 = Vector([-2.029,9.97,4.172])
vector_2 = Vector([-9.231,-6.639,-7.245])
print vector_1.check_parallel(vector_2)
print vector_1.check_orthogonal(vector_2)

vector_1 = Vector([-2.328,-7.284,-1.214])
vector_2 = Vector([-1.821,1.072,-2.94])
print vector_1.check_parallel(vector_2)
print vector_1.check_orthogonal(vector_2)

vector_1 = Vector([2.118,4.827])
vector_2 = Vector([0,0])
print vector_1.check_parallel(vector_2)
print vector_1.check_orthogonal(vector_2)

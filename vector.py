from math import sqrt, acos , pi
from decimal import Decimal, getcontext

getcontext().prec = 5

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
        return abs(abs(self.dot_product(v)) - self.magnitude() * \
            v.magnitude()) < tolerance

    def check_orthogonal(self,v,tolerance=1e-10):
        return abs(self.dot_product(v)) < tolerance

    def parallel_component(self, v):
        try:

            return (v.normalized()).times_scalar(self.dot_product(v.normalized()))
        except Exception as e:
            if str(e) == self.CANNOT_NORMALIZE_ZERO_VECTOR_MSG:
                raise Exception(self.NO_UNIQUE_PARALLEL_COMPONENT_MSG)
            else:
                raise e

    def orth_component(self, v):
        try:
            return self.minus(self.parallel_component(v))
        except Exception as e:
            if str(e) == self.NO_UNIQUE_PARALLEL_COMPONENT_MSG:
                raise Exception(self.NO_UNIQUE_PARALLEL_COMPONENT_MSG)
            else:
                raise e



    def cross_product(self, v):

        try:
            x1,y1,z1 = self.coordinates
            x2,y2,z2 = v.coordinates
            product = [y1*z2-y2*z1,-(x1*z2-x2*z1),x1*y2-x2*y1]
            return Vector(product)

        except Exception as e:
            if len(self.coordinates)==2 and len(v.coordinates) ==2:
                u1 = [x for x in self.coordinates]
                u2 = [x for x in v.coordinates]
                print u1
                print u2
                u1.append(0)
                u2.append(0)
                print u1
                print u2
                return Vector(u1).cross_product(Vector(u2))
            elif len(self.coordinates) !=3 or len(v.coordinates) !=3:
                raise Exception ('not dimension not equal or not enough value')


    def area_of_parallelogram(self,v):
        return self.cross_product(v).magnitude()







vector_1 = Vector([8.462,7.893])
vector_2 = Vector([6.984,-5.975])
print vector_1.cross_product(vector_2)

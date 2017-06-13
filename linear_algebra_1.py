import math
class Vector(object):
    def __init__(self, coordinates):
        try:
            if not coordinates:
                raise ValueError
            self.coordinates = tuple(coordinates)
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
        new_coordinates = [c*x for x in self.coordinates]
        return Vector(new_coordinates)
    
    def magnitude(self):
        coordinates_squared = [x**2 for x in self.coordinates]
        return (sum(coordinates_squared))**0.5

    def normalize(self):
        try:
            magnitude = self.magnitude()
            new_coordinates = [x/magnitude for x in self.coordinates]
            return new_coordinates
        
        except ZeroDivisionError:
            raise Exception('Can not normalize the zero vector')



#verctor_1 = Vector([8.218,-9.341])
#verctor_2 = Vector([-1.129,2.111])
#print Vector.plus(verctor_1,verctor_2)
"""
verctor_3 = Vector([7.119,8.215])
verctor_4 = Vector([-8.223,0.878])
print Vector.minus(verctor_3,verctor_4)

verctor_5 = Vector([1.671,-1.012,-0.318])
print Vector.times_scalar(verctor_5, 7.41)


verctor_6 = Vector([-0.221,7.437])
print Vector.magnitude(verctor_6)

verctor_7 = Vector([8.813,-1.331,-6.247])
print Vector.magnitude(verctor_7)

"""
verctor_8 = Vector([5.581,-2.136])
print verctor_8
print verctor_8.normalize()

verctor_9 = Vector([1.996,3.108,-4.554])
print verctor_9.normalize()

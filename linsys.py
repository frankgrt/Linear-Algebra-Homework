from decimal import Decimal, getcontext
from copy import deepcopy

from vector import Vector
from plane import Plane

getcontext().prec = 30


class LinearSystem(object):

    ALL_PLANES_MUST_BE_IN_SAME_DIM_MSG = 'All planes in the system should live in the same dimension'
    NO_SOLUTIONS_MSG = 'No solutions'
    INF_SOLUTIONS_MSG = 'Infinitely many solutions'

    def __init__(self, planes):
        try:
            d = planes[0].dimension
            for p in planes:
                assert p.dimension == d

            self.planes = planes
            self.dimension = d

        except AssertionError:
            raise Exception(self.ALL_PLANES_MUST_BE_IN_SAME_DIM_MSG)


    def swap_rows(self, row1, row2):
        self[row2],self[row1] = self[row1],self[row2]


    def multiply_coefficient_and_row(self, coefficient, row):
        n = self[row].normal_vector
        new_normal_vector = n.times_scalar(coefficient)
        new_constant_term = self[row].constant_term * coefficient
        self[row] = Plane(normal_vector=new_normal_vector,
                                 constant_term=new_constant_term)


    def add_multiple_times_row_to_row(self, coefficient, row_to_add, row_to_be_added_to):

        vector_to_add = self[row_to_add].normal_vector.times_scalar(coefficient)
        k_to_add = self[row_to_add].constant_term * coefficient
        vector_tobe_add = self[row_to_be_added_to].normal_vector
        k_tobe_add = self[row_to_be_added_to].constant_term

        new_vector = vector_to_add.plus(vector_tobe_add)
        new_k = k_to_add + k_tobe_add

        self[row_to_be_added_to] = Plane(normal_vector = new_vector,
                                            constant_term = new_k)
    """
    def sorting(system):
        while True:
            indices = system.indices_of_first_nonzero_terms_in_each_row()
            a = 0
            for i in range(len(system)-1):
                if indices[i] > indices[i+1] or indices[i] < 0:
                    system.swap_rows(i,i+1)
                    a += 1
            if a == 0:
                break

        return system

    def compute_triangular_form(self):
        system = deepcopy(self)

            # check coefficient, and remove coefficient if needed.

        while True:

            system.sorting()
            print system
            indices = system.indices_of_first_nonzero_terms_in_each_row()
            a = 0
            for i in range(len(indices)):
                if indices[0] < 0 :
                    break
                if indices[i] == indices[i-1]:
                    coefficient = - system[i].normal_vector.coordinates[indices[i]] / (system[i-1].normal_vector.coordinates[indices[i-1]])
                    system.add_multiple_times_row_to_row(coefficient,i-1,i)
                    a += 1
                    break
            if a == 0:
                break

        return system


    """
    def compute_triangular_form(self):
        system = deepcopy(self)
        rows = len(system)
        cols = system.dimension
        for i,p in enumerate(system):
            while i < cols:
                if p.normal_vector.coordinates[i] == 0:
                    for k in range(i+1, rows):
                        if system[k].normal_vector.coordinates[i] != 0:
                            system.swap_rows(i,k)
                            break
                break

            for j in range(i+1, rows):
                coefficient = -system[j].normal_vector.coordinates[i]/system[i].normal_vector.coordinates[i]
                system.add_multiple_times_row_to_row(coefficient,i,j)


        return system




    def indices_of_first_nonzero_terms_in_each_row(self):
        num_equations = len(self)
        num_variables = self.dimension

        indices = [-1] * num_equations

        for i,p in enumerate(self.planes):
            try:
                indices[i] = p.first_nonzero_index(p.normal_vector.coordinates)
            except Exception as e:
                if str(e) == Plane.NO_NONZERO_ELTS_FOUND_MSG:
                    continue
                else:
                    raise e

        return indices


    def __len__(self):
        return len(self.planes)


    def __getitem__(self, i):
        return self.planes[i]


    def __setitem__(self, i, x):
        try:
            assert x.dimension == self.dimension
            self.planes[i] = x

        except AssertionError:
            raise Exception(self.ALL_PLANES_MUST_BE_IN_SAME_DIM_MSG)


    def __str__(self):
        ret = 'Linear System:\n'
        temp = ['Equation {}: {}'.format(i+1,p) for i,p in enumerate(self.planes)]
        ret += '\n'.join(temp)
        return ret




class MyDecimal(Decimal):
    def is_near_zero(self, eps=1e-10):
        return abs(self) < eps

p1 = Plane(normal_vector=Vector(['1','1','1']), constant_term='1')
p2 = Plane(normal_vector=Vector(['0','1','1']), constant_term='2')
s = LinearSystem([p1,p2])
t = s.compute_triangular_form()
if not (t[0] == p1 and
        t[1] == p2):
    print 'test case 1 failed'
    print t

p1 = Plane(normal_vector=Vector(['1.7','1','1']), constant_term='1')
p2 = Plane(normal_vector=Vector(['1.3','1.3','1']), constant_term='2')
s = LinearSystem([p1,p2])
t = s.compute_triangular_form()
if not (t[0] == p1 and
        t[1] == Plane(constant_term='1')):
    print 'test case 2 failed'
    print t
p1 = Plane(normal_vector=Vector(['1','1','1']), constant_term='1')
p2 = Plane(normal_vector=Vector(['0','1','0']), constant_term='2')
p3 = Plane(normal_vector=Vector(['1.3','1','-1']), constant_term='3')
p4 = Plane(normal_vector=Vector(['1.9','0','-2']), constant_term='2')
s = LinearSystem([p1,p2,p3,p4])
t = s.compute_triangular_form()
if not (t[0] == p1 and
        t[1] == p2 and
        t[2] == Plane(normal_vector=Vector(['0','0','-2']), constant_term='2') and
        t[3] == Plane()):
    print 'test case 3 failed'
    print t

p1 = Plane(normal_vector=Vector(['0','1','1']), constant_term='1')
p2 = Plane(normal_vector=Vector(['1.3','-1','1']), constant_term='2')
p3 = Plane(normal_vector=Vector(['1.9','2','-5']), constant_term='3')
s = LinearSystem([p1,p2,p3])
t = s.compute_triangular_form()
if not (t[0] == Plane(normal_vector=Vector(['1','-1','1']), constant_term='2') and
        t[1] == Plane(normal_vector=Vector(['0','1','1']), constant_term='1') and
        t[2] == Plane(normal_vector=Vector(['0','0','-9']), constant_term='-2')):
    print 'test case 4 failed'
    print t

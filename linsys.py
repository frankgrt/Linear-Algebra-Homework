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

    def compute_triangular_form(self):
        system = deepcopy(self)
        a = True
        while a == True:
            # sort Equations

            b= True
            while b == True:
                indices = system.indices_of_first_nonzero_terms_in_each_row()
                is_swaped = False
                for i in range(len(system)-1):
                    if indices[i] >= indices[i+1] or indices[i] < 0:
                        system.swap_rows(i,i+1)
                        is_swaped = True

                if is_swaped == False:
                    b = False

            # check coefficient, and remove coefficient if needed.

            for i,p in enumerate(indices):
                #is_add_row_to_row = False
                if p < 0:
                    break
                if p < i:
                    coefficient = - system[i].normal_vector.coordinates[p] / (system[p].normal_vector.coordinates[p])
                    system.add_multiple_times_row_to_row(coefficient,i-1,i)
                    #is_add_row_to_row = True
                    break
                a = False






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


p0 = Plane(normal_vector=Vector(['1','1','1']), constant_term='1')
p1 = Plane(normal_vector=Vector(['0','1','0']), constant_term='2')
p2 = Plane(normal_vector=Vector(['0','1','-1']), constant_term='3')
p3 = Plane(normal_vector=Vector(['1','0','-2']), constant_term='2')


s = LinearSystem([p0,p1,p2,p3])

print s.compute_triangular_form()

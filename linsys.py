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
            # if the first nonzero index is not i, swap
            while i < cols:
                if p.normal_vector.coordinates[i] == 0:
                    for k in range(i+1, rows):
                        if system[k].normal_vector.coordinates[i] != 0:
                            system.swap_rows(i,k)
                            break
                break
            # use the number i row to eliminate the coefficient of index before
            # i index for each row below the number i row
            for j in range(i+1, rows):
                if system[i].normal_vector.coordinates[i] != 0:
                    coefficient = -system[j].normal_vector.coordinates[i]/ \
                                system[i].normal_vector.coordinates[i]
                    system.add_multiple_times_row_to_row(coefficient,i,j)

        return system

    """
    # use algorethem from myself
    def compute_rref(self):
        tf = self.compute_triangular_form()
        # change the first nonzero coefficient to 1
        for i in range(min(len(tf),tf.dimension)):
            coefficient = Decimal(tf[i].normal_vector.coordinates[i])
            if coefficient != 0:
                new_normal_vector = tf[i].normal_vector.\
                      times_scalar(Decimal(1.0)/coefficient)
                new_constant_term = tf[i].constant_term / coefficient
                tf[i] = Plane(normal_vector=new_normal_vector, \
                       constant_term=new_constant_term)

        # for each row, eliminate other coeffictient after first nonzero index
        for i,p in enumerate(tf):
            row = p.normal_vector.coordinates
            dimension = len(row)
            if i < dimension:
                for j in range(i+1,min(len(tf),tf.dimension)):
                    coefficient = Decimal(- tf[i].normal_vector.coordinates[j])
                    tf.add_multiple_times_row_to_row(coefficient,j,i)
            if i > dimension:
                tf.add_multiple_times_row_to_row(-1,dimension,i)

        return tf


    """


    def compute_rref(self):
        tf = self.compute_triangular_form()
        rows = len(tf)
        cols = tf.dimension
        indices = tf.indices_of_first_nonzero_terms_in_each_row()

        for i in range(rows)[::-1]:
            if indices[i] < 0:
                continue
            coefficient_1 = tf[i].normal_vector.coordinates[indices[i]]
            new_normal_vector = tf[i].normal_vector.times_scalar(Decimal(1/coefficient_1))
            new_constant_term = tf[i].constant_term / coefficient_1
            tf[i] = Plane(normal_vector=new_normal_vector, constant_term=new_constant_term)
            #print tf[i]
            for j in range(i)[::-1]:
                coefficient_2 = -tf[j].normal_vector.coordinates[indices[i]]

                tf.add_multiple_times_row_to_row(coefficient_2,i,j)
        return tf


    def compute_solution(self):
        rref = self.compute_rref()
        try:
            rref.raise_no_solution_error()
            rref.raise_infinit_solution_error()
        except Exception as e:
            if str(e) == self.NO_SOLUTIONS_MSG or str(e) == self.INF_SOLUTIONS_MSG:
                return str(e)
        solutions_coordinate = [rref[i].constant_term for i in range(rref.dimension)]
        return Vector(solutions_coordinate)

    def raise_no_solution_error(self):
        pivot_indices = self.indices_of_first_nonzero_terms_in_each_row()
        for i,p in enumerate(pivot_indices):
            b = MyDecimal(self[i].constant_term)
            if p==-1 and (not b.is_near_zero()):
                raise Exception(self.NO_SOLUTIONS_MSG)

    def raise_infinit_solution_error(self):
        pivot_indices = self.indices_of_first_nonzero_terms_in_each_row()
        num_pivots = sum([1 if index >= 0 else 0 for index in pivot_indices])
        num_variables = self.dimension
        if num_pivots < num_variables:
            raise Exception(self.INF_SOLUTIONS_MSG)



    """
    def compute_solution(self):
        try:
            return self.do_gaussian_elimination_and_extract_solution()

        except Exception as e:
            if (str(e) == self.NO_SOLUTIONS_MSG or
                 str(e) == self.INF_SOLUTIONS_MSG):
                 return str(e)
            else:
                raise e

    def do_gaussian_elimination_and_extract_solution(self):
        rref = self.compute_rref()

        rref.raise_exception_if_contradictory_equation()
        rref.raise_exception_if_too_few_pivots()

        num_variables = rref.dimension
        solution_coordinates = [rref.planes[i].constant_term for i in
                                range(num_variables)]
        return Vector(solution_coordinates)

    def raise_exception_if_contradictory_equation(self):
        for p in self.planes:
            try:
                p.first_nonzero_index(p.normal_vector.coordinates)

            except Exception as e:
                if str(e) == 'No nonzero elements found':
                    constant_term = MyDecimal(p.constant_term)
                    if not constant_term.is_near_zero():
                        raise Exception(self.NO_SOLUTIONS_MSG)
                else:
                    raise e

    def raise_exception_if_too_few_pivots(self):
        pivot_indices = self.indices_of_first_nonzero_terms_in_each_row()
        num_pivots = sum([1 if index >= 0 else 0 for index in pivot_indices])
        num_variables = self.dimension

        if num_pivots < num_variables:
            raise Exception(self.INF_SOLUTIONS_MSG)
    """


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

class Parametrization(object):

    BASEPT_AND_DIR_VECTORS_MUST_BE_IN_SAME_DIM_MSG = ('The basepoint and direction vectors should all live in the same')
    def __init__(self, basepoint, direction_vectors):

        self.basepoint = basepoint
        self.direction_vectors = direction_vectors
        self.dimension = self.basepoint.dimension

        try:
            for v in direction_vectors:
                assert v.dimension == self.dimension
        except AssertionError:
            raise Exception(BASEPT_AND_DIR_VECTORS_MUST_BE_IN_SAME_DIM_MSG)




p1 = Plane(normal_vector=Vector(['0.786','0.786','0.588']), constant_term='-0.714')
p2 = Plane(normal_vector=Vector(['-0.138','-0.138','0.244']), constant_term='0.319')
s = LinearSystem([p1,p2])
r = s.compute_rref()
print r

p1 = Plane(normal_vector=Vector(['8.631','5.112','-1.816']), constant_term='-5.113')
p2 = Plane(normal_vector=Vector(['4.315','11.132','-5.27']), constant_term='-6.775')
p3 = Plane(normal_vector=Vector(['-2.158','3.01','-1.727']), constant_term='-0.831')
s = LinearSystem([p1,p2,p3])
r = s.compute_rref()

print r

p1 = Plane(normal_vector=Vector(['0.935','1.76','-9.365']), constant_term='-9.955')
p2 = Plane(normal_vector=Vector(['0.187','0.352','-1.873']), constant_term='-1.991')
p3 = Plane(normal_vector=Vector(['0.374','0.704','-3.746']), constant_term='3.982')
p4 = Plane(normal_vector=Vector(['-0.561','-1.056','5.619']), constant_term='5.973')

s = LinearSystem([p1,p2,p3,p4])
r = s.compute_rref()

print r

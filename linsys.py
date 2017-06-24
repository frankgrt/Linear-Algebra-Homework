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

            if coefficient_1 !=0:
                new_normal_vector = tf[i].normal_vector.times_scalar(Decimal(1/coefficient_1))
                new_constant_term = tf[i].constant_term / coefficient_1
                tf[i] = Plane(normal_vector=new_normal_vector, constant_term=new_constant_term)

            for j in range(i)[::-1]:
                coefficient_2 = -tf[j].normal_vector.coordinates[indices[i]]
                tf.add_multiple_times_row_to_row(coefficient_2,i,j)
        return tf


    def compute_solution(self):
        rref = self.compute_rref()
        try:
            rref.raise_no_solution_error()
            rref.check_infinit_solution()
        except Exception as e:
            if str(e) == self.NO_SOLUTIONS_MSG:
                return str(e)
            if str(e) == self.INF_SOLUTIONS_MSG:
                return rref.compute_parametriztion()

        solutions_coordinate = [rref[i].constant_term for i in range(rref.dimension)]
        return Vector(solutions_coordinate)

    def raise_no_solution_error(self):
        pivot_indices = self.indices_of_first_nonzero_terms_in_each_row()
        for i,p in enumerate(pivot_indices):
            b = MyDecimal(self[i].constant_term)
            if p==-1 and (not b.is_near_zero()):
                raise Exception(self.NO_SOLUTIONS_MSG)

    def check_infinit_solution(self):
        pivot_indices = self.indices_of_first_nonzero_terms_in_each_row()
        num_pivots = sum([1 if index >= 0 else 0 for index in pivot_indices])
        num_variables = self.dimension
        if num_pivots < num_variables:
            raise Exception(self.INF_SOLUTIONS_MSG)


    def compute_parametriztion(self):

        rows = len(self)
        cols = self.dimension

        #convert plane object to list of list
        matrix = []
        k_list = []
        for i,p in enumerate(self):
            each_row = []
            k_list = []
            for k in p.normal_vector.coordinates:
                each_row.append(k)
            each_row.append(p.constant_term)
            matrix.append(each_row)

        if rows > cols:
            for i in range(rows - cols):
                matrix.pop()

        #add "0" row if rows < cols
        add_row = [Decimal("0") for i in range(cols+1)]
        if len(matrix) < cols:
            for j,h in enumerate(matrix):
                a = MyDecimal(h[j]-1)

                if not a.is_near_zero():
                    matrix.insert(j,add_row)

        #add -1
        for l,m in enumerate(matrix):
            m[l] += -1

        # construct basepoint vector
        basepoint_matrix = []
        for i in matrix:
            basepoint_matrix.append(i[-1])
        basepoint = Vector(basepoint_matrix)

        # construct direction vectors
        direction_vectors_matrix = []
        for i in range(1,cols):
            direction_vectors_matrix_row = []
            for j in range(len(matrix)):
                direction_vectors_matrix_row.append(-matrix[j][i])
            row = Vector(direction_vectors_matrix_row)
            direction_vectors_matrix.append(row)

        p = Parametrization(basepoint, direction_vectors_matrix)

        return p



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
        self.dimension = basepoint.dimension

        try:
            for v in direction_vectors:
                assert v.dimension == self.dimension
        except AssertionError:
            raise Exception(BASEPT_AND_DIR_VECTORS_MUST_BE_IN_SAME_DIM_MSG)

    def __str__(self):
        dimension = self.dimension
        d = self.direction_vectors

        # if all coordinates in a direction vetor is 0, delete this vector
        for i,p in enumerate(d):
            count= 0
            for j in p.coordinates:
                k = MyDecimal(j)
                if k.is_near_zero():
                    count +=1
            if count == p.dimension:
                del(d[i])

        #initiate output string
        output = ''

        #construct each row of output
        for i in range(dimension):
            output += "x_" + str(i+1)
            output += ' = '
            output += str(round(self.basepoint.coordinates[i],3))
            output += ' + '
            for j,p in enumerate(d):
                output += str(round(p.coordinates[i],3))
                output += ' t_'+str(j)
                if j < len(d)-1:
                    output += ' + '
            output += "\n"

        return output




"""
p1 = Plane(normal_vector=Vector(['1','1','0']), constant_term='-1.326')
p2 = Plane(normal_vector=Vector(['0','0','1']), constant_term='0.558')
s = LinearSystem([p1,p2])
t = s.compute_parametriztion()

print t
print "*****************************************************"



p1 = Plane(normal_vector=Vector(['1','0','0.091']), constant_term='-0.301')
p2 = Plane(normal_vector=Vector(['1','0','-0.509']), constant_term='-0.492')
p3 = Plane(normal_vector=Vector(['0','0','0']), constant_term='0')
s = LinearSystem([p1,p2,p3])
t = s.compute_parametriztion()

print t
print "*****************************************************"



p1 = Plane(normal_vector=Vector(['1','1.882','-10.016']), constant_term='-10.647')
p2 = Plane(normal_vector=Vector(['0','0','0']), constant_term='0')
p3 = Plane(normal_vector=Vector(['0','0','0']), constant_term='0')
p4 = Plane(normal_vector=Vector(['0','0','0']), constant_term='0')

s = LinearSystem([p1,p2,p3,p4])
t = s.compute_parametriztion()
print t
print "*****************************************************"

"""




p1 = Plane(normal_vector=Vector(['0.786','0.786','0.588']), constant_term='-0.714')
p2 = Plane(normal_vector=Vector(['-0.138','-0.138','0.244']), constant_term='0.319')
s = LinearSystem([p1,p2])
t = s.compute_solution()


print t


p1 = Plane(normal_vector=Vector(['8.631','5.112','-1.816']), constant_term='-5.113')
p2 = Plane(normal_vector=Vector(['4.315','11.132','-5.27']), constant_term='-6.775')
p3 = Plane(normal_vector=Vector(['-2.158','3.01','-1.727']), constant_term='-0.831')
s = LinearSystem([p1,p2,p3])
t = s.compute_rref()
r = t.compute_parametriztion()
print t
print r


p1 = Plane(normal_vector=Vector(['0.935','1.76','-9.365']), constant_term='-9.955')
p2 = Plane(normal_vector=Vector(['0.187','0.352','-1.873']), constant_term='-1.991')
p3 = Plane(normal_vector=Vector(['0.374','0.704','-3.746']), constant_term='-3.982')
p4 = Plane(normal_vector=Vector(['-0.561','-1.056','5.619']), constant_term='5.973')

s = LinearSystem([p1,p2,p3,p4])
t = s.compute_rref()
r = t.compute_parametriztion()
print t
print r

from decimal import Decimal, getcontext

from vector import Vector

getcontext().prec = 30


class Hyperplane(object):

    NO_NONZERO_ELTS_FOUND_MSG = 'No nonzero elements found'

    def __init__(self, normal_vector=None, constant_term=None):
        self.dimension = 3

        if not normal_vector:
            all_zeros = [0]*self.dimension
            normal_vector = Vector(all_zeros)
        self.normal_vector = normal_vector

        if not constant_term:
            constant_term = Decimal(0)
        self.constant_term = Decimal(constant_term)

        self.set_basepoint()

    def is_parallel(self, v):
        n1 = self.normal_vector
        n2 = v.normal_vector

        return n1.is_parallel(n2)

    def set_basepoint(self):
        try:
            n = self.normal_vector
            c = self.constant_term
            basepoint_coords = [0]*self.dimension

            initial_index = Hyperplane.first_nonzero_index(n.coordinates)
            initial_coefficient = n.coordinates[initial_index]

            basepoint_coords[initial_index] = float(c)/float(initial_coefficient)
            self.basepoint = Vector(basepoint_coords)

        except Exception as e:
            if str(e) == Hyperplane.NO_NONZERO_ELTS_FOUND_MSG:
                self.basepoint = None
            else:
                raise e

    def __eq__(self, v):
        if self.normal_vector.is_zero():
            if not v.normal_vector.is_zero():
                return False
            else:
                diff = self.constant_term - v.constant_term
                return MyDecimal(diff).is_near_zero()
        elif v.normal_vector.is_zero():
            return False

        if not self.is_parallel(v):
            return False

        x0 = self.basepoint
        y0 = v.basepoint
        difference_between_points = x0.minus(y0)

        return difference_between_points.is_orthogonal(self.normal_vector)

    def __str__(self):

        num_decimal_places = 3

        def write_coefficient(coefficient, is_initial_term=False):
            coefficient = round(coefficient, num_decimal_places)
            if coefficient % 1 == 0:
                coefficient = int(coefficient)

            output = ''

            if coefficient < 0:
                output += '-'
            if coefficient > 0 and not is_initial_term:
                output += '+'

            if not is_initial_term:
                output += ' '

            if abs(coefficient) != 1:
                output += '{}'.format(abs(coefficient))

            return output

        n = self.normal_vector

        try:
            initial_index = Hyperplane.first_nonzero_index(n.coordinates)
            terms = [write_coefficient(n.coordinates[i], is_initial_term=(i==initial_index)) + 'x_{}'.format(i+1)
                     for i in range(self.dimension) if round(n.coordinates[i], num_decimal_places) != 0]
            output = ' '.join(terms)

        except Exception as e:
            if str(e) == self.NO_NONZERO_ELTS_FOUND_MSG:
                output = '0'
            else:
                raise e

        constant = round(self.constant_term, num_decimal_places)
        if constant % 1 == 0:
            constant = int(constant)
        output += ' = {}'.format(constant)

        return output


    @staticmethod
    def first_nonzero_index(iterable):
        for k, item in enumerate(iterable):
            if not MyDecimal(item).is_near_zero():
                return k
        raise Exception(Hyperplane.NO_NONZERO_ELTS_FOUND_MSG)


class MyDecimal(Decimal):
    def is_near_zero(self, eps=1e-10):
        return abs(self) < eps


def main():
    hyperplane1 = Hyperplane(normal_vector=Vector([-0.412, 3.806, 0.728]), constant_term=-3.46)
    hyperplane2 = Hyperplane(normal_vector=Vector([1.03, -9.515, -1.82]), constant_term=8.65)
    print('Is parallel = ' + str(hyperplane1.is_parallel(hyperplane2)))
    print('Equal = ' + str(hyperplane1 == hyperplane2) + '\n')

    hyperplane3 = Hyperplane(normal_vector=Vector([2.611, 5.528, 0.283]), constant_term=4.6)
    hyperplane4 = Hyperplane(normal_vector=Vector([7.715, 8.306, 5.342]), constant_term=3.76)
    print('Is parallel = ' + str(hyperplane3.is_parallel(hyperplane4)))
    print('Equal = ' + str(hyperplane3 == hyperplane4) + '\n')

if __name__ == "__main__":
    main()

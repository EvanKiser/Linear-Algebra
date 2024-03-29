from decimal import Decimal, getcontext

from vector import Vector

getcontext().prec = 30


class Plane(object):

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

            initial_index = Plane.first_nonzero_index(n.coordinates)
            initial_coefficient = n.coordinates[initial_index]

            basepoint_coords[initial_index] = float(c)/float(initial_coefficient)
            self.basepoint = Vector(basepoint_coords)

        except Exception as e:
            if str(e) == Plane.NO_NONZERO_ELTS_FOUND_MSG:
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
            initial_index = Plane.first_nonzero_index(n.coordinates)
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
        raise Exception(Plane.NO_NONZERO_ELTS_FOUND_MSG)


class MyDecimal(Decimal):
    def is_near_zero(self, eps=1e-10):
        return abs(self) < eps


def main():
    plane1 = Plane(normal_vector=Vector([-0.412, 3.806, 0.728]), constant_term=-3.46)
    plane2 = Plane(normal_vector=Vector([1.03, -9.515, -1.82]), constant_term=8.65)
    print('Is parallel = ' + str(plane1.is_parallel(plane2)))
    print('Equal = ' + str(plane1 == plane2) + '\n')

    plane3 = Plane(normal_vector=Vector([2.611, 5.528, 0.283]), constant_term=4.6)
    plane4 = Plane(normal_vector=Vector([7.715, 8.306, 5.342]), constant_term=3.76)
    print('Is parallel = ' + str(plane3.is_parallel(plane4)))
    print('Equal = ' + str(plane3 == plane4) + '\n')

    plane5 = Plane(normal_vector=Vector([-7.926, 8.625, -7.212]), constant_term=-7.952)
    plane6 = Plane(normal_vector=Vector([-2.642, 2.875, -2.404]), constant_term=-2.443)
    print('Is parallel = ' + str(plane5.is_parallel(plane6)))
    print('Equal = ' + str(plane5 == plane6) + '\n')

if __name__ == "__main__":
    main()

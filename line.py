from decimal import Decimal, getcontext

from vector import Vector

getcontext().prec = 30


class Line(object):

    NO_NONZERO_ELTS_FOUND_MSG = 'No nonzero elements found'

    def __init__(self, normal_vector=None, constant_term=None):
        self.dimension = 2

        if not normal_vector:
            all_zeros = ['0']*self.dimension
            normal_vector = Vector(all_zeros)
        self.normal_vector = normal_vector

        if not constant_term:
            constant_term = Decimal('0')
        self.constant_term = Decimal(constant_term)

        self.set_basepoint()


    def set_basepoint(self):
        try:
            n = self.normal_vector
            c = self.constant_term
            basepoint_coords = ['0']*self.dimension

            initial_index = Line.first_nonzero_index(n)
            initial_coefficient = n[initial_index]

            basepoint_coords[initial_index] = c/initial_coefficient
            self.basepoint = Vector(basepoint_coords)

        except Exception as e:
            if str(e) == Line.NO_NONZERO_ELTS_FOUND_MSG:
                self.basepoint = None
            else:
                raise e

    #Two lines are parallel if their normal vectors are parallel
    def is_parallel(self, v):
        if (self.normal_vector.is_parallel(v.normal_vector)):
            return True
        else:
            return False

    def is_equal(self, v):
        #Two lines that are equal must be parallel
        if not self.is_parallel(v):
            return False
        #Two lines are equal if the line between two 
        else:
            return True

    def compute_intersection(self, v):
        if self.is_parallel(v):
            return None
        else:
            # X = (Dk1 - Bk2) / (AD - BC)
            xNumerator = (v.normal_vector[1] * self.constant_term) - (self.normal_vector[1] * v.constant_term)
            xDenominator = (self.normal_vector[0] * v.normal_vector[1]) - (self.normal_vector[1] * v.normal_vector[0])
            x = xNumerator/xDenominator

            # Y = (-Ck1 + Ak2) / (AD - BC)
            yNumerator = (-v.normal_vector[0] * self.constant_term) + (self.normal_vector[0] * v.constant_term)
            yDenominator = (self.normal_vector[0] * v.normal_vector[1]) - (self.normal_vector[1] * v.normal_vector[0])
            y = yNumerator/yDenominator
            return([x,y])
        

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
            initial_index = Line.first_nonzero_index(n)
            terms = [write_coefficient(n[i], is_initial_term=(i==initial_index)) + 'x_{}'.format(i+1)
                     for i in range(self.dimension) if round(n[i], num_decimal_places) != 0]
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
        raise Exception(Line.NO_NONZERO_ELTS_FOUND_MSG)


class MyDecimal(Decimal):
    def is_near_zero(self, eps=1e-10):
        return abs(self) < eps


def main():
    line1 = Line(Vector([4.046, 2.836]), 1.21)
    line2 = Line(Vector([10.115, 7.09]), 3.025)
    print('Same line = ' + line1.is_equal(line2))
    print('Is parallel = ' + line1.is_parallel(line2))
    print('Intersection = ' + line1.compute_intersection(line2))

    line3 = Line(Vector([7.204, 3.182]), 8.68)
    line4 = Line(Vector([8.172, 4.114]), 9.883)
    print('Same line = ' + line3.is_equal(line4))
    print('Is parallel = ' + line3.is_parallel(line4))
    print('Intersection = ' + line3.compute_intersection(line4))

    line5 = Line(Vector([1.182, 5.562]), 6.744)
    line6 = Line(Vector([1.773, 8.343]), 9.525)
    print('Same line = ' + line5.is_equal(line6))
    print('Is parallel = ' + line5.is_parallel(line6))
    print('Intersection = ' + line5.compute_intersection(line6))

if __name__ == "__main__":
    main()

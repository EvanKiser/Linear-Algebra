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

    #Two lines are parallel if their normal vectors are parallel
    def is_parallel(self, v):
        n1 = self.normal_vector
        n2 = v.normal_vector
        
        return n1.is_parallel(n2)
    
    #Setting basepoint by setting an index to 0 (0, k/B) or (k/A, 0)
    def set_basepoint(self):
        try:
            n = self.normal_vector
            c = self.constant_term
            basepoint_coords = [0]*self.dimension

            initial_index = Line.first_nonzero_index(n.coordinates)
            initial_coefficient = n.coordinates[initial_index]

            basepoint_coords[initial_index] = float(c)/initial_coefficient
            self.basepoint = Vector(basepoint_coords)

        except Exception as e:
            if str(e) == Line.NO_NONZERO_ELTS_FOUND_MSG:
                self.basepoint = None
            else:
                raise e

    def __eq__(self, v):
        #Two lines that are equal must be parallel
        if not self.is_parallel(v):
            return False
        #Two lines are equal if the line between two points is orthogonal to the normal vector
        x0 = self.basepoint
        y0 = v.basepoint
        difference_between_points = x0.minus(y0)

        return difference_between_points.is_orthogonal(self.normal_vector)

    def compute_intersection(self, v):
        if self.is_parallel(v):
            return None
        else:
            # X = (Dk1 - Bk2) / (AD - BC)
            x_numerator = (v.normal_vector.coordinates[1] * float(self.constant_term)) - (self.normal_vector.coordinates[1] * float(v.constant_term))
            x_denominator = (self.normal_vector.coordinates[0] * v.normal_vector.coordinates[1]) - (self.normal_vector.coordinates[1] * v.normal_vector.coordinates[0])
            x = x_numerator/x_denominator

            # Y = (-Ck1 + Ak2) / (AD - BC)
            y_numerator = (-v.normal_vector.coordinates[0] * float(self.constant_term)) + (self.normal_vector.coordinates[0] * float(v.constant_term))
            y_denominator = (self.normal_vector.coordinates[0] * v.normal_vector.coordinates[1]) - (self.normal_vector.coordinates[1] * v.normal_vector.coordinates[0])
            y = y_numerator/y_denominator
            return(Vector([x,y]))
        

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
    line1 = Line(normal_vector=Vector([4.046, 2.836]), constant_term=1.21)
    line2 = Line(normal_vector=Vector([10.115, 7.09]), constant_term=3.025)
    print('Is parallel = ' + str(line1.is_parallel(line2)))
    print('Same line = ' + str(line1 == line2))
    print('Intersection = ' + str(line1.compute_intersection(line2)) + '\n')

    line3 = Line(normal_vector=Vector([7.204, 3.182]), constant_term=8.68)
    line4 = Line(normal_vector=Vector([8.172, 4.114]), constant_term=9.883)
    print('Is parallel = ' + str(line3.is_parallel(line4)))
    print('Same line = ' + str(line3 == line4))
    print('Intersection = ' + str(line3.compute_intersection(line4)) + '\n')

    line5 = Line(normal_vector=Vector([1.182, 5.562]), constant_term=6.744)
    line6 = Line(normal_vector=Vector([1.773, 8.343]), constant_term=9.525)
    print('Is parallel = ' + str(line5.is_parallel(line6)))
    print('Same line = ' + str(line5 == line6))
    print('Intersection = ' + str(line5.compute_intersection(line6)) + '\n')

if __name__ == "__main__":
    main()

import sys
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

    #String function for vectors
    def __str__(self):
        return 'Vector: {}'.format(self.coordinates)

    #Two Vectors are equivalent if they have the same coordinates
    def __eq__(self, v):
        return self.coordinates == v.coordinates

    #The overall total amount of change by the two vectors
    def plus(self, v):
        
        #The vectors being added must have the same amount of coordinates
        if (self.dimension != v.dimension):
            raise Exception("Dimensions of both vectors must be equivalent")

        #Adding vectors is the same as the sum of their coordinates
        sumCoordinates = []
        for x in range(0,self.dimension):
            sumCoordinates.append(self.coordinates[x] + v.coordinates[x])
        
        return Vector(tuple(sumCoordinates))

    #The vector that runs from the head of one vector to the head of the other vector
    def minus(self, v):

        #The vectors being subtracted must have the same amount of coordinates
        if (self.dimension != v.dimension):
            raise Exception("Dimensions of both vectors must be equivalent")

        #Subtracting vectors is the same as the difference of their coordinates
        diffCoordinates = []
        for x in range(0,self.dimension):
            diffCoordinates.append(self.coordinates[x] - v.coordinates[x])

        return Vector(tuple(diffCoordinates))

    #The dot product is the angel between two different vectors
    def dot_product(self, v):

        #The vectors being multiplied must have the same amount of coordinates
        if (self.dimension != v.dimension):
            raise Exception("Dimensions of both vectors must be equivalent")

        #dot product is calculated by multiplying the corresponding coordinates of two vectors
        dotProduct = 0
        for x in range(0, self.dimension):
            dotProduct += self.coordinates[x] * v.coordinates[x]

        return dotProduct


    #Multipling the vecotr by a given scalar
    def times_scalar(self, scalar):
        scale_coordinates = []
        for x in range(0, self.dimension):
            scale_coordinates.append(self.coordinates[x] * scalar)

        return Vector(tuple(scale_coordinates))

    #magnitude is the length of a vector
    def magnitude(self):

        sumOfSquares = 0
        #The magnitude of a vector is equal to the square root of the sum of the coordinates of the vector squared 
        for x in range(0, self.dimension):
            sumOfSquares += math.pow(self.coordinates[x],2)
         
        return math.sqrt(sumOfSquares)

    '''
    ' calculating the unit vector of a given vector
    ' (1/magnitude)(vector)
    '''
    def normalization(self):
        magnitude = self.magnitude()

        #The zero vector cannot be normalized
        if (magnitude == 0):
            raise Exception("The zero vector has no direction")
        inverseMagnitude = 1/self.magnitude()
        return self.times_scalar(inverseMagnitude)

    def angle_between(self, v, radians=True):
        if self.magnitude() == 0 or v.magnitude() == 0:
            raise Exception("The zero vector has no direction")

        dotproduct = self.dot_product(v)
        if radians == True:
            return math.acos(round(dotproduct/(self.magnitude() * v.magnitude()), 6))

        else:
            return math.degrees(dotproduct/(self.magnitude() * v.magnitude()))

    #Two vectors are orthogonal if their dot_product is zero
    def is_orthogonal(self, v, tolerance=1e-10):

        #The zero vector is orthogonal with all other vectors
        for x in range(0, self.dimension):
            if self.coordinates[x] != 0:
                break
            else:
                return True
        for x in range(0, v.dimension):
            if v.coordinates[x] != 0:
                break
            else:
                return True

        return abs(self.dot_product(v)) < tolerance

    def is_zero(self, tolerance=1e-10):
        return self.magnitude() < tolerance
        
    #Two vectors are parallel if 
    def is_parallel(self, v):

        #The zero vector is orthogonal with all other vectors
        for x in range(0, self.dimension):
            if self.coordinates[x] != 0:
                break
            else:
                return True     
        for x in range(0, v.dimension):
            if v.coordinates[x] != 0:
                break
            else:
                return True

        #Two vectors are parrallel if one is a scalar multiple of the other
        if (self.angle_between(v) == 0) or (self.angle_between(v) == math.pi):
            return True
        else:
            return False

    def component_parallel_to(self, basis):
        #v parrallel to a basis is equal to the normalization of the basis vector times the scalar of the dot proudct of v and the normalized basis
        u = basis.normalization()
        return u.times_scalar((self.dot_product(u)))

    def component_orthogonal_to(self, basis):
        return self.minus(self.component_parallel_to(basis))

    def cross_product(self, v):
        if self.dimension != 3 or v.dimension != 3:
            raise Exception("vectors must be of the third dimension")

        newVec = []
        newVec.append((self.coordinates[1] * v.coordinates[2]) - (v.coordinates[1] * self.coordinates[2]))
        newVec.append(-((self.coordinates[0] * v.coordinates[2]) - (v.coordinates[0] * self.coordinates[2])))
        newVec.append((self.coordinates[0] * v.coordinates[1]) - (v.coordinates[0] * self.coordinates[1]))
        return Vector(tuple(newVec))
    
    def area_of_parallelogram(self, v):
        return self.cross_product(v).magnitude()

    def area_of_triangle(self ,v):
        return self.area_of_parallelogram(v) * .5





def main():
    vector1 = Vector([8.218, -9.341])
    vector2 = Vector([-1.129, 2.111])
    print(vector1.plus(vector2))

    vector3 = Vector([7.119, 8.215])
    vector4 = Vector([-8.223, 0.878])
    print(vector3.minus(vector4))

    vector5 = Vector([1.671, -1.012, -0.318])
    print(vector5.times_scalar(7.41))

    vector6 = Vector([-0.221, 7.437])
    print(vector6.magnitude())

    vector7 = Vector([8.813, -1.331, -6.247])
    print(vector7.magnitude())

    vector8 = Vector([5.581,-2.136,])
    print(vector8.normalization())

    vector9 = Vector([1.996, 3.108, - 4.554])
    print(vector9.normalization())

    vector10 = Vector([7.887, 4.138])
    vector11 = Vector([-8.802, 6.776])
    print(vector10.dot_product(vector11))

    vector12 = Vector([-5.955, -4.904, -1.874])
    vector13 = Vector([-4.496, -8.755, 7.103])
    print(vector12.dot_product(vector13))

    vector14 = Vector([3.183, -7.627])
    vector15 = Vector([-2.668, 5.319])
    print(vector14.angle_between(vector15, radians=True))

    vector16 = Vector([7.35, 0.221, 5.188])
    vector17 = Vector([2.751, 8.259, 3.985])
    print(vector16.angle_between(vector17, radians=False))

    vector18 = Vector([-7.579, -7.88])
    vector19 = Vector([22.737, 23.64])
    print("Orthogonal: " + str(vector18.is_orthogonal(vector19)))
    print("Parallel: " + str(vector18.is_parallel(vector19)))

    vector20 = Vector([-2.029, 9.97, 4.172])
    vector21 = Vector([-9.231, -6.639, -7.45])
    print("Orthogonal: " + str(vector20.is_orthogonal(vector21)))
    print("Parallel: " + str(vector20.is_parallel(vector21)))

    vector22 = Vector([-2.328, -7.284, -1.214])
    vector23 = Vector([-1.821, 1.072, -2.94])
    print("Orthogonal: " + str(vector22.is_orthogonal(vector23)))
    print("Parallel: " + str(vector22.is_parallel(vector23)))

    vector24 = Vector([.118, 4.827])
    vector25 = Vector([0, 0])
    print("Orthogonal: " + str(vector24.is_orthogonal(vector25)))
    print("Parallel: " + str(vector24.is_parallel(vector25)))

    vector26 = Vector([3.039, 1.879])
    vector27 = Vector([0.825, 2.036])
    print(vector26.component_parallel_to(vector27))

    vector28 = Vector([-9.88, -3.264, -8.159])
    vector29 = Vector([-2.155, -9.353, -9.473])
    print(vector28.component_orthogonal_to(vector29))

    vector30 = Vector([3.009, -6.172, 3.692, -2.51])
    vector31 = Vector([6.404, -9.144, 2.759, 8.718])
    print(vector30.component_parallel_to(vector31))
    print(vector30.component_orthogonal_to(vector31))

    vector32 = Vector([8.462, 7.893, -8.187])
    vector33 = Vector([6.984, -5.975, 4.778])
    print(vector32.cross_product(vector33))

    vector34 = Vector([-8.987, -9.838, 5.031])
    vector35 = Vector([-4.268, -1.861, -8.866])
    print(vector34.area_of_parallelogram(vector35))

    vector36 = Vector([1.5, 9.547, 3.691])
    vector37 = Vector([-6.007, 0.124, 5.772])
    print(vector36.area_of_triangle(vector37))



    

if __name__ == "__main__":
    main()

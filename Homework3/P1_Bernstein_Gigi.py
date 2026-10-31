from numbers import Real
from typing import Sequence 
from typing import List
from typing import Union
from typing import overload
from testif import testif

class NVector:
    def __init__(self, *num_seq) -> None:
        ''' create a vector from either a sequence or seperate numbers
        preconditions: 
            - must have at least one argument
            - must contain only real numbers
        postconditions: 
            - the vector is created with the given elements'''
        num_list = []
        if len(num_seq) == 0:
            raise TypeError("must have at least one argument")
        if len(num_seq) == 1:
            first_arg = num_seq[0]
            if isinstance(first_arg, (list, tuple)): # if input is list or tuple
                self._elements: List[Real] = list(first_arg)
            else:
                self._elements = [first_arg]
        else: # more than one argument was given
            self._elements = list(num_seq)

        for element in self._elements:
            if not isinstance(element, Real):
                raise TypeError("all elements must be a real number")

    def __len__(self) -> int:
        '''returns the length of the vector.'''
        return len(self._elements)

    def __getitem__(self, index) -> int:
        '''return item at index, negative numbers work like standard lists
        parameters: 
            index - the integer of the requested elements place
        raises:
            TypeError: if index is not valid list index
            IndexError: if index is outside valid range of list'''
        return self._elements[index]

    def __setitem__(self, index, value) -> None:
        '''set item at index, negative numbers work like standard lists
        parameters:
            index - the integer of the requested elements place
            value - the new value to set at the given index
        raises:
            TypeError: if index is not valid list index or value is not a real number
            IndexError: if index is outside valid range of list'''
        if not isinstance(value, Real):
            raise TypeError("value must be a real number")
        self._elements[index] = value

    def __str__(self) -> str:
        '''returns a string representation of the vector.
        parameters:
            none
        returns:
            str - the string representation of the vector'''
        return str(self._elements)

    def __eq__(self, other) -> bool:
        '''returns True if the vectors are equal, False otherwise.
        parameters:
            other - the other vector to compare with
        returns:
            bool - True if the vectors are equal, False otherwise'''
        if not isinstance(other, NVector):
            return False
        return self._elements == other._elements 

    def __ne__(self, other) -> bool:
        '''returns True if the vectors are not equal, False otherwise.
        parameters:
            other - the other vector to compare with
        returns:
            bool - True if the vectors are not equal, False otherwise'''
        return not self.__eq__(other)

    def __add__(self, other) -> "NVector":
        '''returns the sum of two vectors.
        parameters:
            other - the other vector to add
        returns:
            NVector - the sum of the two vectors'''
        if not isinstance(other, NVector):
            raise TypeError("other must be an NVector")
        if len(self._elements) != len(other._elements):
            raise ValueError("vectors must have the same length")
        return NVector(*[a + b for a, b in zip(self._elements, other._elements)])

    def __radd__(self, other) -> "NVector":
        '''returns the sum of two vectors from the right.
        parameters:
            other - the other vector to add
        returns:
            NVector - the sum of the two vectors'''
        return self.__add__(other)

    def __mul__(self, scalar) -> "NVector":
        '''returns the scalar multiplication of the vector.
        parameters:
            scalar - the scalar to multiply the vector by
        returns:
            NVector - the resulting vector after scalar multiplication'''
        if not isinstance(scalar, Real):
            raise TypeError("scalar must be a real number")
        return NVector(*[a * scalar for a in self._elements])

    def __rmul__(self, scalar) -> "NVector":
        '''returns the scalar multiplication of the vector from the right.
        parameters:
            scalar - the scalar to multiply the vector by
        returns:
            NVector - the resulting vector after scalar multiplication'''
        return self.__mul__(scalar)

    def zeros(self, n: int) -> "NVector":
        '''returns a vector of zeros with the specified length.
        parameters:
            n - the length of the vector
        returns:
            NVector - the vector of zeros'''
        if not isinstance(n, int) or n <= 0:
            raise ValueError("n must be a positive integer")
        return NVector(*[0] * n)

def main() -> None:
    print("Z Number: Z23652485")
    """Run checks for NVector using the testif helper."""
    vector = NVector(1, 2, 3, 4)
    sequence_vector = NVector([1, 2, 3, 4])
    other_vector = NVector(4, 3, 2, 1)

    testif(vector == sequence_vector, "sequence constructor", "vectors match", "vectors do not match")
    testif(len(vector) == 4, "__len__ works", "length is 4", "length is not 4")
    testif(vector[2] == 3, "__getitem__ works", "index 2 is 3", "index 2 is not 3")

    vector[3] = 10
    testif(vector[3] == 10, "__setitem__ works", "index 3 is 10", "index 3 was not updated")
    testif(str(vector) == "[1, 2, 3, 10]", "__str__ works", "string is correct", "string is incorrect")
    testif(vector != other_vector, "__ne__ works", "vectors differ", "vectors should differ")
    testif(vector + other_vector == NVector(5, 5, 5, 11), "__add__ works", "sum is correct", "sum is incorrect")
    testif(vector.__radd__(other_vector) == NVector(5, 5, 5, 11), "__radd__ works", "sum is correct", "sum is incorrect")
    testif(vector * 2 == NVector(2, 4, 6, 20), "__mul__ works", "product is correct", "product is incorrect")
    testif(2 * vector == NVector(2, 4, 6, 20), "__rmul__ works", "product is correct", "product is incorrect")
    testif(vector.zeros(3) == NVector(0, 0, 0), "zeros works", "three zeros returned", "incorrect zero vector")


if __name__ == "__main__":
    main()
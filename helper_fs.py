from math import gcd
### Subtracts two vectors;
### returns result
def matr_vect(matr,vect):
    for i in matr:
        print (sproduct(i,vect))
def subtract(vect1, vect2):
    tmp=[]
    for i in range(0,len(vect1)):
        tmp.append(vect1[i]-vect2[i])
    return tmp

### Multiplies a vector by a number;
### retruns a new vector
def num_vect(times,vect):
    tmp = []
    for i in vect:
        tmp.append(i*times)
    return tmp

### find the greatest common devisor? of a vector;
### returns int
def gcd_vector(vector):
    if len(vector)==0:
        return 1;
    else:
        result = vector[0]
        for p in range(1,len(vector)):
            result = gcd (result,vector[p])
    return result

### optimises vector, by deviding all of its members to their gcd
### see gcd_vector
### returns a new vector
def optimise_vector(vect):
    reductor = gcd_vector(vect)
    if reductor > 1:
        for i in range(0,len(vect)):
            vect[i] =vect[i]//reductor
    return vect


### sumproduct of vectors;
### returns int
def sproduct(arr1,arr2):
    summ=0
    if len(arr1) == len(arr2):
        for i in range (0,len(arr1)):
            summ= summ + arr1[i]*arr2[i]
    else:
        print ("vector length mismatch")
    return summ
### finds lowest common multiple of two numbers;
### returns int
def lcm(a, b):
    return int(abs(a*b) /gcd(a,b))

### function finds the nmber of zeros in a line
### returns nuber of zeros in provided vector
def zeros(vect):
    p = 0
    for i in vect:
        if i == 0:
            p+=1
    return p
### finds number of elements that have values on the same indexes
### used in acessing how many of the variables in a line have a value in the solution
### returns the number of in a an array
def exist_in_both(source,loc):
    matches = 0
    if len(source) != len(loc):
        return -1
    for i in range(0,len(source)):
        if source[i] != 0 and loc[i] != 0:
            matches+=1
    return matches

### finction that detects the number of lines that are full of zeros
### returns int, number of lines of zeros
def full_zero_lines(matr):
    if len(matr)==0:
        return []
    if len(matr[0])==0:
        return []
    len_line=len(matr[0])
    z_lines=0
    for i in matr:
        if zeros(i) == len_line:
            z_lines+=1
    return z_lines
### function that returns indexes of the the non-zero values in the provided vector
### returns an array of indexes
def find_indexes(vect):
    arr = []
    for i in range(0,len(vect)):
        if vect[i] !=0:
            arr.append(i)
    return arr

### function that in the context of a solution vector and another that is ana equesion,
### provides the index of the element that 0 in the solution, but it's a non sezro in the equesion
### reurns int, as the index
def find_missing_index(vect, sol):
    for i in range(0,len(vect)):
        if vect[i] !=0 and sol[i]==0:
            return i

### function that finds number of solutions
### delta of size of matrix + numbers lines full of zeres =>
### if result is one then its the general case
### if result is more than one, ones should be added ustomatically to
### the solution vector
def solutions(matrix):
    return abs(len(matrix)-len(matrix[0])) + full_zero_lines(matrix)


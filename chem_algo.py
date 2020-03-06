from math import gcd
#t = [[1, 2, -2, -1], [2, 0, -1, 0], [6, 0, 0, -2]]
#t2 = [[0, 0, 2, 0, 0, 0, -2], [1, 1, 0, 0, 0, -2, 0], [0, 1, 0, 0, -1, 0, 0], [0, 4, 4, 0, -4, -4, -1], [0, 0, 1, 0, -1, -1, 0], [1, 0, 0, -2, 0, 0, 0]]
#table = [[4, 0, -1, 0], [10, 0, 0, -2],[0, 2, -2, -1]]
#strange = [[1,0,-1,-1],[0,2,-2,-1]]
#strange2 = [[2,0,-2],[0,2,-1],[0,2,-1]]

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
### called wehn the pivvot elemnet of the gauss method is a 0
### to optimise the matrix
### returns matrix
def optimise_gauss(matr,ind):
    tmp = []
    for i in range(ind,len (matr)):
        if matr[i][ind]!= 0:
            tmp = matr[i]
            matr[i]= matr[ind]
            matr[ind] = tmp
    return matr

### reduces matrix by the gauss method + optimises each line after calculatons
### returns reduced matrix
def gauss_reduction(hmatrix):
    for i in range(0,len(hmatrix)-1):
        if hmatrix[i][i] == 0:
            hmatrix=optimise_gauss(hmatrix,i) 
        for j in range(i+1,len(hmatrix)):
            if  hmatrix[i][i] != 0 and hmatrix[j][i] !=0:
                devisor = int(lcm(hmatrix[i][i],hmatrix[j][i]))
                c1 = int(devisor // hmatrix[i][i])
                c2 = int(devisor // hmatrix[j][i])
                hmatrix[j] = optimise_vector(subtract(num_vect(c1,hmatrix[i]),num_vect(c2,hmatrix[j])))
    
    for i in range(len(hmatrix)-1,0,-1):
        ### gauss optimisation here is not needed beacuse after the first cycle all pivots are(should be) set
        for j in range(i-1,-1,-1):
            if hmatrix[i][i] != 0 and hmatrix[j][i] !=0:
                devisor = int(lcm(hmatrix[i][i],hmatrix[j][i]))
                c1 = int(devisor // hmatrix[i][i])
                c2 = int(devisor // hmatrix[j][i])
                hmatrix[j] = optimise_vector(subtract(num_vect(c1,hmatrix[i]),num_vect(c2,hmatrix[j])))
    return(hmatrix)

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


### functiin that solves the equesion system
def int_chem_matrix_kernel(matrix):
    matrix = gauss_reduction(matrix)
    if len(matrix)==0:
        return []
    if len(matrix[0])==0:
        return []

    sol = [0] * len(matrix[0])
    num_comb =  solutions(matrix)  
    if num_comb>1:
        for p in range(len(matrix),len(matrix[0])):
            sol[p] = 1 
    not_solved = True
    line_len = len(matrix[0])
    rows = len(matrix)
    line = 0 
    factors = 0
    failsafe = 0

    while(zeros(sol)!=0):
        failsafe+=1
        assert(failsafe <= 100)
        factors = line_len - zeros(matrix[line]) 
        matches = exist_in_both(matrix[line],sol)
        if factors == 2 and matches == 0:
            fact = find_indexes(matrix[line])
            ### we know that all of the indexes are coprime, because of the optimisation
            ### therefore we can just exchange their absolute values and be done with it 
            sol[fact[0]] = abs (matrix[line][fact[1]])
            sol[fact[1]] = abs (matrix[line][fact[0]])
        elif factors - matches == 1 and matches !=0:
            ### general case of an equesion where all but one variables is known
            missing = find_missing_index(matrix[line],sol)
            complement = sproduct(sol,matrix[line])
            common = abs(lcm(matrix[line][missing],complement))
            sol = num_vect(abs(int(common/complement)),sol)
            sol[missing] = abs(int(common/matrix[line][missing]))
        line+=1
        line=line%rows
    sol=optimise_vector(sol)
    return (sol)
### function that given a matrix returns a kernel of the matrix, where all its members are integers
### returns a vector
def get_integer_kernel(matr):
    return int_chem_matrix_kernel(matr)

#print(get_integer_kernel(t))
#print(get_integer_kernel(t2))
#print(get_integer_kernel(table))
#print(get_integer_kernel(strange))
#print(get_integer_kernel(strange2))

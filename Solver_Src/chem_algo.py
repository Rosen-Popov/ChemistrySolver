from helper_fs import *
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
    matr_sq=min([len(hmatrix[0]),len(hmatrix)])
    for i in range(0,matr_sq-1):
        if hmatrix[i][i] == 0:
            hmatrix=optimise_gauss(hmatrix,i)
        for j in range(i+1,matr_sq):
            if  hmatrix[i][i] != 0 and hmatrix[j][i] !=0:
                devisor = int(lcm(hmatrix[i][i],hmatrix[j][i]))
                c1 = int(devisor // hmatrix[i][i])
                c2 = int(devisor // hmatrix[j][i])
                hmatrix[j] = optimise_vector(subtract(num_vect(c1,hmatrix[i]),num_vect(c2,hmatrix[j])))

    for i in range(matr_sq-1,0,-1):
        ### gauss optimisation here is not needed beacuse after the first cycle all pivots are(should be) set
        for j in range(i-1,-1,-1):
            try:
                if hmatrix[i][i] != 0 and hmatrix[j][i] !=0:
                    devisor = int(lcm(hmatrix[i][i],hmatrix[j][i]))
                    c1 = int(devisor // hmatrix[i][i])
                    c2 = int(devisor // hmatrix[j][i])
                    hmatrix[j] = optimise_vector(subtract(num_vect(c1,hmatrix[i]),num_vect(c2,hmatrix[j])))
            except:
                print("prolblematic: ",i,j, len(hmatrix[i]),len(hmatrix[j]),len(hmatrix))
    return(hmatrix)

### functiin that solves the equesion system
def int_chem_matrix_kernel(matrix):
    matrix = gauss_reduction(matrix)
    if len(matrix)==0:
        return []
    if len(matrix[0])==0:
        return []

    sol = [0] * len(matrix[0])
    print("2")
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
    print (sol)
    return (sol)
### function that given a matrix returns a kernel of the matrix, where all its members are integers
### returns a vector
def get_integer_kernel(matr):
    return int_chem_matrix_kernel(matr)

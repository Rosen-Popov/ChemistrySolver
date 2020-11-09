#!/usr/bin/python3
import re
import chem_algo
import sys
###     given a chemical reaction returns the compounds inside it, and which isde they are on
###     fixes the array begore that as well
def ret_compounds(reaction):
    tmp = reaction.replace(' ','').replace('>','')
    tmp = tmp.split('-')
    result = []
    pos = tmp[0].split('+')
    neg = tmp[1].split('+')
    for i in pos:
        result.append([i.lstrip("0123456789"),1])
    for i in neg:
        result.append([i.lstrip("0123456789"),-1])
    return result

###     removes brackets from bracketed formulas
def remove_br(string):
    return string.strip("1234567890").strip("()")

def extract(struct):
    comp = struct[0]
    mod = struct[1]
    chem_regex = "([A-Z][a-z]?[0-9]*)|([(].*[)][0-9]*)"
    num_regex = "[0-9]*\Z"
    x = re.findall(chem_regex, comp)
    for i in range(len(x)):
        x[i] = list(x[i])
        x[i] = list(filter(None, x[i]))
        mod = re.findall(num_regex, x[i][0])
        mod.append('1')
        mod = list(filter(None,mod))
        x[i] = [remove_br(x[i][0]), int(mod[0])]

    return x

###     checks if something is an element or a compound
###     returns true or false
def check_if_element(Element):
    elem = 0
    for i in Element[0]:
        if "A" <= i <= "Z":
            elem += 1
        if elem >1:
            return False
        return True


class chemical:
    def __init__(self,chem,side):
        self._elements = dict()
        self._matser_compound = [chem,1]
        self._side = side

    def desolve_compound(self):
        loc_que=[self._matser_compound]
        for chem in loc_que:
            tmp=extract(chem)
            for member in tmp:
                if check_if_element(member):
                    if member[0] in self._elements:
                        self._elements[str(member[0])].append(int(member[1])*int(chem[1]))
                    else:
                        self._elements.update({member[0]:[int(member[1])*int(chem[1])]})
                else:
                    loc_que.append(member)
            loc_que.pop(0)

        for chem in self._elements.keys():
            print(chem)
            self._elements[chem] = sum(self._elements[chem])


class chemical_reaction:
    def __init__(self,reaction):
        self._compounds_list = ret_compounds(reaction)
        self._comp = []
        self._vector = [1] * len(self._compounds_list)
        self._chem_set = set()
        self._made_table = False
        self._sol = ""
        for i in self._compounds_list:
            self._comp.append(chemical(i[0],i[1]))
        for i in self._comp:
            i.desolve_compound()
            for el in i._elements.keys():
                self._chem_set.add(el)
        self._matrix =[[] for i in range (len(self._chem_set))]

    def make_table(self):
        self._made_table = True
        p =0
        for i in self._chem_set:
            for j in range (len(self._comp)):
                if i in self._comp[j]._elements.keys():
                    self._matrix[p].append(self._comp[j]._elements[i]*self._comp[j]._side)
                else:
                    self._matrix[p].append(0)
            p+=1

    def solve_eq(self):
        if self._made_table == False:
            self.make_table()
            self._vector = chem_algo.get_integer_kernel(self._matrix)
            tmp_format_string_list =[]
            added_arrow = False
            length = len(self._vector)
            for i in range(length):
                if added_arrow == False and 1<i < length and self._comp[i]._side == -1:
                    added_arrow = True
                    tmp_format_string_list.append('-> ')
                else:
                    if i!=0:
                        tmp_format_string_list.append('+ ')

                tmp_format_string_list.append(str(self._vector[i]))
                tmp_format_string_list.append('*')
                tmp_format_string_list.append(self._compounds_list[i][0])
                tmp_format_string_list.append(' ')

            self._sol=''.join(tmp_format_string_list)
            return self._sol

    def get_res(self):
        return self._sol

if __name__ == "__main__":
    if "--test" in sys.argv or "-t" in sys.argv:
        import csv
        number_of_tests =0
        failed_tests = 0
        succ_tests = 0
        incorrect_output = 0
        with open('tests.csv', newline='') as csvfile:
            tests = csv.reader(csvfile, delimiter=',',quotechar=';')
            for line  in tests:
                number_of_tests = number_of_tests + 1
                try:
                    p=chemical_reaction(line[0])
                    if p.solve_eq().replace(' ','') == line[1].replace(' ',''):
                        succ_tests = succ_tests + 1
                    else:
                        print(line[0],"<>\nres: ",p.get_res(),"\nans:",line[1])
                        incorrect_output = incorrect_output + 1
                except:
                    failed_tests = failed_tests + 1
                    print("not doable ", line[0])


    test=chemical_reaction("HNO3 + Cu -> Cu(NO3)2 + H2O + NO")
    test.solve_eq()
    print(extract("NO3"))
    print(test.get_res())

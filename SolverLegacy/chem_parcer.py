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

#def deb(string):
#    chem_regex = "([A-Z][a-z]?[0-9]*)|([(].*[)][0-9]*)"
#    num_regex = "[0-9]*\Z"
#    x = re.findall(chem_regex, comp)

def extract(struct):
    comp = struct[0]
    global_mod = struct[1]
    chem_regex = r"([A-Z][a-z]?[0-9]*)|([(].*[)][0-9]*)"
    num_regex = r"[0-9]*\Z"
    x = re.findall(chem_regex, comp)
    for i in range(len(x)):
        x[i] = list(x[i])
        x[i] = list(filter(None, x[i]))
        mod = re.findall(num_regex, x[i][0])
        mod.append('1')
        mod = list(filter(None,mod))
        x[i] = [remove_br(x[i][0]), int(mod[0])*global_mod]
    return x

###     checks if something is an element or a compound
###     returns true or false
def check_if_element(Element):
    elem = 0
    for i in Element[0]:
        if 'A' <= i <= 'Z':
            elem += 1
    if elem >1:
        return False
    else:
        return True



class Chemical:
    def __init__(self,chem,side):
        self._elements = dict()
        self._matser_compound = [chem,1]
        self._side = side

    def IntoElemnets(self):
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
                    tmp.extend(extract(member))
            loc_que.pop(0)
        for chem in self._elements.keys():
            self._elements[chem] = sum(self._elements[chem])


class ChemicalReaction:
    def __init__(self,reaction):
        self._compounds_list = ret_compounds(reaction)
        self._comp = []
        self._vector = [1] * len(self._compounds_list)
        self._chem_set = set()
        self._made_table = False
        self._sol = ""
        for i in self._compounds_list:
            self._comp.append(Chemical(i[0],i[1]))
        for i in self._comp:
            i.IntoElemnets()
            for el in i._elements.keys():
                self._chem_set.add(el)
        self._matrix =[[] for i in range (len(self._chem_set))]

    def MakeTable(self):
        self._made_table = True
        p =0
        for i in self._chem_set:
            for j in range (len(self._comp)):
                if i in self._comp[j]._elements.keys():
                    self._matrix[p].append(self._comp[j]._elements[i]*self._comp[j]._side)
                else:
                    self._matrix[p].append(0)
            p+=1

    def SolveEq(self):
        if self._made_table == False:
            print("1")
            self.MakeTable()
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

def SolveAndPrint(chemical):
    test=ChemicalReaction(chemical)
    print(test.SolveEq())


def print_stats(categ,all_tests,succ,incorrect,failed):
    if len(categ)>0:
        print(categ)
    print("Passed :{}/{} - {}%".format(succ,all_tests,int((succ/all_tests)*100) ))
    print("Total Failure :{}/{} - {}%".format(failed,all_tests,int((failed/all_tests)*100) ))
    print("Incorrect Results :{}/{} - {}%".format(incorrect,all_tests,int((incorrect/all_tests)*100) ))

#if __name__ == "__main__":
#    if "--test" in sys.argv or "-t" in sys.argv:
#        import csv
#        number_of_tests =0
#        failed_tests = 0
#        succ_tests = 0
#        incorrect_output = 0
#        with open('tests.csv', newline='') as csvfile:
#            tests = csv.reader(csvfile, delimiter=',',quotechar=';')
#            for line  in tests:
#                number_of_tests = number_of_tests + 1
#                try:
#                    p=ChemicalReaction(line[0])
#                    sol = p.SolveEq().replace(' ','')
#                    #print(sol)
#                    #if sol == line[1].replace(' ',''):
#                        #succ_tests = succ_tests + 1
#                    #else:
#                    print(line[0],"<>\nres: ",p.get_res(),"\nans:",line[1])
#                    incorrect_output = incorrect_output + 1
#                except:
#                    failed_tests = failed_tests + 1
#                    print("not doable ", line[0])
#        print_stats("Tests",number_of_tests,succ_tests,incorrect_output,failed_tests)
#
#    if "--interactive" in sys.argv or "-i" in sys.argv:
#        print("Reaction ? =")
#        SolveAndPrint(input())
#        ### NOTE! possible buffer overflow with this 
#    elif "--pipe" in sys.argv or "-p" in sys.argv:
#        number_of_tests =0
#        failed_tests = 0
#        succ_tests = 0
#        incorrect_output = 0
#        for line  in sys.stdin:
#            number_of_tests = number_of_tests + 1
#            try:
#                p=ChemicalReaction(line[0])
#                if p.SolveEq().replace(' ','') == line[1].replace(' ',''):
#                    succ_tests = succ_tests + 1
#                else:
#                    print(line[0],"<>\nres: ",p.get_res(),"\nans:",line[1])
#                    incorrect_output = incorrect_output + 1
#            except:
#                failed_tests = failed_tests + 1
#                print("not doable ", line[0])
#        print_stats("Stdin",number_of_tests,succ_tests,incorrect_output,failed_tests)
print(extract(["(OH)2(OH)2",1]))

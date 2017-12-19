'''
    Biblioteca de funcoes necessarias para tranformar sentensas para CNF
    Segundo Projeto de IASD
    IST - 12/2017
    Pedro Henrique Silva
    Andre Baiao
'''
#######





#############Test Functions#############
def isAtom(line):
    '''
Receives a line already in list format and returns True
if it is a Atom, false otherwise
'''
    
    if (len(line) == 1):#if the line is a single litera "A"
        return True
    elif ((line[0] == 'not') and ((len(line[1]) == 1))):#if it is a nagation of a literal(not,A)
        return True
    else:
         return False

def isNegation(line):
    '''
    Tests if a line is a nagation but not an atom, ex ~(A or B) returns True, ~A False
'''
    if (line[0] == "not") and not(isAtom(line)):
        return True
    else:
        return False
    
def isDisj(line):
    '''
    Test if it is a simple disjunction ,A or B, which A & B are both atom
    if yes return TRUE
    '''
    
    if line[0] == "or":
        for k in line[1:]:
            if not(isAtom(k)):
                return False
        return True
    else :
        return False
    
def isCNF(line):
    '''
    Test if line is in CNF
'''
    if isDisj(line) or isAtom(line):
        return True
    else:
        return False

#################################################
############Simplification Functions#############
    
def implication(line):
    '''
A=>B = ~A or B
'''
    A = line[1]
    B = line[2]
    return ('or',('not',A),B)


def equivalence(line):
    '''
A<=>B = (~A or B) and (A or ~B)
'''
    A = line[1]
    B = line[2]
    return('and',('or',("not",A),B),('or',A,("not",B)))


def demorgans(line) :
    '''
    Applies Demorgans laws to given line,
    ~(A or B) =  ~A and ~B
    ~(A and B) =  ~A or ~B
'''
    
    A = line[1][1]
    B = line[1][2] 
    if (line[1][0] == "or"):#tests if it is a negation of an AND or OR
           return ("and",("not",A),("not",B))
    else:####elif line[1][0]==and
           return("or",("not",A),("not",B))

def doubleNeg(line):
    '''
    (not, (not,A)) -> A  
'''
    if line[1][0] == "not":
        return line[1][1]
    else:
        return line
    
def separator(_list):
    lista = []
    for line in _list:
        if (line[0] == "and"):
            _list.append((line[1]))
            _list.append((line[2]))
            _list.remove(line)

def CNF_TESTER(_list):
    for line in _list:
        if not(isCNF(line)):
            return False
    return True

def distributivity(line):

    component1 = line[1]
    component2 = line[2]
    if (component1[0]=="and" and component2[0] == "and"):
        return (("and", ("and", ("and",("or", component1[1],component2[1]),("or", component1[1],component2[2])),("or", component1[2],component2[1])),("or", component1[2],component2[2])))
    elif component1[0]=="and" and isAtom(component2):
        return ("and",("or",component1[1],component2),("or",component1[2],component2))
    elif component2[0]=="and" and isAtom(component1):
        return ("and",("or",component2[1],component1),("or",component2[2],component1))
    



def converter(_list):
    '''
    Converter takes the initial statements, in a list format, and returns
    the convertion to cnf of the entire list

    '''
    test = False
    while not(test):
        for line in _list:
            if (line[0] == "<=>"):
                _list.append(equivalence(line))
                _list.remove(line)

            elif(line[0] == "=>"):
                _list.append(implication(line))
                _list.remove(line)
                

            elif(line[0] == "or" and not(isCNF(line))):
                _list.append(distributivity(line))
                _list.remove(line)  

            elif(line[0] == "not" and not(isCNF(line))):
                if (doubleNeg(line) == line):#se não for uma double negation
                    _list.append(demorgans(line))
                    _list.remove(line)    
                _list.append(doubleNeg(line))# elimina double negation
                _list.remove(line)
        separator(_list)
        test = CNF_TESTER(_list)


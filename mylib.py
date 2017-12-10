'''
    Biblioteca de funcoes necessarias para tranformar sentensas para CNF
    Segundo Projeto de IASD
    IST - 12/2017
    Pedro Henrique Silva
    Andre Baiao
'''
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
    for line in _list:
        if line[0] == "and":
            #print(line[1])
            _list.append((line[1]))
            #print(line[2])
            _list.append((line[2]))
            _list.remove(line)

    
        
        

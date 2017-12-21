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
    if (line[0] == "not") and not(len(line[1]==1)) and len(line)==2:
        return True
    else:
        return False

def isDisj(line):
    '''
    Test if it is a simple disjunction ,A or B, which A & B are both atom
    if yes return TRUE
    '''
    if isAtom(line):
        return True
    elif line[0] == "or":
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
    return (isDisj(line) or isAtom(line))

def CNF_TESTER(_list):
    '''
    tests weather a list of logic sentences is in CNF
'''
    for line in _list:
        if not(isCNF(line)):
            return False
    return True
#################################################
############Simplification Functions#############
#################################################

def cleanUp(logic):
    
    result = []
    
    #Treat negation lists as unique literals.
    #No operations to perform on nots
    if logic[0] == 'not':
        return logic
    
    #append the operator 
    result.append(logic[0])
    outer_op = logic[0]
    
    #Loop through the literals
    for i in range(1, len(logic)):
        #if the operator matches to the outer operator
        if logic[i][0] == outer_op:
            #Loop through the literals of this list
            for j in range(1, len(logic[i])):
                result.append(logic[i][j])
        else:
            #append the logic as is
            result.append(logic[i])
            
    return result






def implication(line):
    '''
A=>B = ~A or B
'''
    A = line[1]
    B = line[2]
    
    return ['or',['not',A],B]

    
def equivalence(line):
    '''
A<=>B = (~A or B) and (A or ~B)
'''
    A = line[1]
    B = line[2]
    
    return['and',implication(["=>",A,B]),implication(["=>",B,A])]


def negator(line):
    '''
    Applies Demorgans laws to given line,
    ~(A or B) =  ~A and ~B
    ~(A and B) =  ~A or ~B
    OR
    Simplify Double Negations
    ~(~A) = A
    Hypothesis line[0] == ~
    
'''

    resp = []
    line = list(line)
    if isAtom(line):
        #~A
        return line
    
    if not(isAtom(line)):
        #~(A=>B) or ~(A<=>B)
        if line[1][0] == "<=>":
            line[1] = equivalence(line[1])
        elif line[1][0] =="=>":
            line[1] = implication(line[1])
    
    #Demorgans Law
    if (line[1][0] == "or"):
        resp.append("and")
    elif line[1][0]=="and":
        resp.append("or")
    #Double Negation
    elif line[1][0] == "not":
        return(line[1][1])
    
    #print(line)#degug
    for i in range(1,len(line[1])):
        
        if (len(line[1][i]) > 1):
            resp.append(negator(['not',line[1][i]]))

        else:
            resp.append(['not',line[1][i]])
    return resp
                        
    
def separator(_list):



    
    lista = []
    for line in _list:
        
        if (line[0] == "and") and not(isCNF(line)):
            _list.append((line[1]))
            _list.append((line[2]))
            _list.remove(line)



def distributivity(line):
    '''
(A or (B and C) = (A or B) and (A or C)
'''
   
    component1 = line[1]
    component2 = line[2]
##    print (component1)
##    print("\n")
##    print(component2)
    
    if component1[0] == "<=>":
        component1 = equivalence(component1)
        #print(component1)
    elif component1[0] == "=>":
        component1 = implication(component1)
        #print(component1)    
    if component2[0] == "<=>":
        component2 = equivalence(component2)
        #print(component2)
    elif component2[0] == "=>":
        component2 = implication(component2)
        #print(component2)
    if component1[0] == 'not' :
        component1 = negator(component1)
        #print(component1)
    if component2[0] == 'not' :
        component2 = negator(component2)
    #print(component1)
    #print(component2)
    if component1[0] == 'or':
        component1 = distributivity(component1)
    
    if component2[0] == 'or':
        component2 = distributivity(component2)
        
    if isCNF(component1) and isCNF(component2):
        return(['or',component1,component2])
    
    resp = []
    resp.append('and')
    
    if component1[0] == 'and' and component2[0]=='and':
        resp.append(distributivity(["or",component1[1],component2[1]]))
        resp.append(distributivity(["or",component1[2],component2[1]]))
        resp.append(distributivity(["or",component1[1],component2[2]]))
        resp.append(distributivity(["or",component1[2],component2[2]]))

    else:#Either one is an and
        
        if component1[0] == 'and':
            if(len(line[2]))>2:
                if isDistributionCandidate(component2):
                    component2 = distributivity(componetent2)
                    resp.append(distributivity(["or",component1[1],component2[1]]))
                    resp.append(distributivity(["or",component1[2],component2[1]]))
                    resp.append(distributivity(["or",component1[1],component2[2]]))
                    resp.append(distributivity(["or",component1[2],component2[2]]))
                else:
                    resp.append(distributivity(["or",component1[1],component2]))
                    resp.append(distributivity(["or",component1[2],component2]))
            else:
                resp.append(distributivity(["or",component1[1],component2]))
                resp.append(distributivity(["or",component1[2],component2]))
               
        else:
            if(len(line[1]))>2:
                if isDistributionCandidate(component1):
                    component1 = distributivity(componetent1)
                    resp.append(distributivity(["or",component1[1],component2[1]]))
                    resp.append(distributivity(["or",component1[2],component2[1]]))
                    resp.append(distributivity(["or",component1[1],component2[2]]))
                    resp.append(distributivity(["or",component1[2],component2[2]]))
                else:
                    resp.append(distributivity(["or",component1,component2[1]]))
                    resp.append(distributivity(["or",component1,component2[2]]))
            else:
                resp.append(distributivity(["or",component1,component2[1]]))
                resp.append(distributivity(["or",component1,component2[2]]))

        
    return resp
def isDistributionCandidate(line):
    '''

checks if the logic sentence is a candidate to distribution
return True if it is, Otherwise it returns false

'''
    if line[0] == 'or':
        for i in range(1, len(line)):
            if len(line[i]) > 1:
                if line[i][0] == 'and':
                    return True
    return False


def add(arg,lista):
    
    if not(arg in lista):
        lista.append(arg)

        
def converter(_list):
    '''

    Converter takes the initial statements, in a list format, and returns
    the convertion to cnf of the entire list

    '''
    test = False
    i=1
    resp = []
    while not(test):
        print (_list)
        for line in _list:
            #print (line)
            #if line inCNF
            if (line[0] == "<=>"):
                add(cleanUp(equivalence(line)),_list)
                _list.remove(line)
                #print("from eq: ")
                #print(equivalence(line))

            elif(line[0] == "=>"):
                add(cleanUp(implication(line)),_list)
                _list.remove(line)
                #print("from imp: ")
                #print(implication(line))
                
            elif(line[0] == "or" ):
                
                add(cleanUp(distributivity(line)),_list)
                _list.remove(line)
                #print("from dist: ")
                #print(distributivity(line))
            
            elif(line[0] == "not" and not(isCNF(line))):
                add(cleanUp(negator(line)),_list)
                _list.remove(line)
                #print("from neg: ")
                #print(negator(line))
                   
        separator(_list)
        test = CNF_TESTER(_list)
        
        #print (resp)

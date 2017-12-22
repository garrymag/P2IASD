from mylib import *
'''
USELESS?????
def stract(A):
    if A[0] == "not":
        return(A[1])
    else:
        return(A)
    
def isNot(A):
    if (A[0] == "not"):
        return True
    else:
        return False

    '''
def Not(A):
    return negator(["not",A])



def resolve(logic1, logic2):
    '''
Receives 2 logic statements in CNF and returns solution
 A   A   A
~A   A   B
___________
[]   A  [A,B]

'''
    
    lista = []
    resp = []
    if not(isAtom(logic1)):
        for a in logic1:
            lista.append(a)
    else :
        lista.append(logic1)

    if not(isAtom(logic2)):
        
        for b in logic2:
            lista.append(b)
    else:
        lista.append(logic2)
        
    resp = deepcopy(lista)
    size = len(lista)
    for i in range(0,len(lista)):
        for j in range(0,len(lista)):
            A = lista[i]
            #print(A)
            if i<j:
                if A == Not(lista[j]):
                    resp.remove(A)
                    resp.remove(lista[j])
                elif A == (lista[j]):
                    resp.remove(lista[j])
    return resp
    
def solver(lista):
    '''
Prove A

Lg1
Lg2
.          Returns True if [] false otherwise
.
.
Lgn
______
~A


'''

    
    goal = lista[-1]#want to prove the last statement
    lista.remove(goal)
    #print(goal)
    test = True
    prev = []
    while (test):
        temp = []
        prev = deepcopy(lista)
        #print(prev)
        if len(prev)==1:
            if prev[0] == Not(goal):
                return True
        #print("prev: ",prev)
        for i in range(0,len(lista)):
            for j in range(0,len(lista)):
                if i<j:
                    A = resolve(lista[i],lista[j])
                    if len(A) == 1:
                        A = A[0]
                    
                    print("A: ", A)
                    print("notA: ",Not(A))
                    if A == Not(goal):
                        return True
                    else:
                        temp.append(A)
        lista = deepcopy(temp)
        if lista == prev:
            test = False
    return False
        
        
        



    

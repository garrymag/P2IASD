def isLiteral(line):
    '''
Receives a line already in list format and returns True
if it is a Literal, false otherwise
'''
    if len(line) == 1:#if the line is a single litera "A"
        return True
    elif (line[0] == 'not') and ((len(line[1]) == 1)):#if it is a nagation of a literal(not,A)
        return True
    elif (line[0]  == 'or') and ((len(line[1]) == 1)and len(line[2] == 1) ):#if it is disjuntion of 2 literals
        return True
    else:
         return False


def implication(line):
    A = line[1]
    B = line[2]
    return ('or',('not',A),B)

def equivalence(line):
    A = line[1]
    B = line[2]
    return('and',('<=>',A,B),('<=>',B,A)
def demorgan(line):
    
        

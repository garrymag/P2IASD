def isLiteral(line):
    if len(line) == 1:#if the line is a single litera "A"
        return True
    elif (line[0] == 'not') and ((len(line[1]) == 1)):#if it is a nagation of a literal(not,A)
        return True
    elif (line[0]  == 'or') and ((len(line[1]) == 1)and len(line[2] == 1) ):#if it is disjuntion of 2 literals
        return True
    else:
         return False





def main():
    return isLiteral(('A'))

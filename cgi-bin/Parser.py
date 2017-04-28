#!C:\Python27\Python.exe
import cgitb; cgitb.enable()
import cgi
import re

def __init__():
    return
dataFromJS = cgi.FieldStorage()
print("Content-Type: text/html\n\n")
codeLines = dataFromJS.list[0].value.split('\n')
allVars = []
startLine = -1
stepCounter = 1
steps = []
lineMax = len(codeLines)-1
outputString = '{"lines":['


def getNextLine(line, count):
    global startLine
    newVarName = ""
    newVarVal = 0
    if line.find("static void Main(") != -1:
        startLine = count
        return False
    line = untab(line)
    if line[:2] == "//": #if the line is a comment, do nothing
        return False
    if searcher(line, "int", "I", 0, count) or searcher(line, "string", "S", "null", count):
        return True
    
def variableChangeSearch(lineNum):
    global outputString
    if lineNum >= lineMax or lineNum >=300:
        outputString = outputString[:-1]
        outputString += ']}'
        print(outputString)
        return
    line = codeLines[lineNum]
    line = untab(line)  
    if line.find(';') == -1 or getNextLine(line, lineNum):
        variableChangeSearch(lineNum+1)
        return
    firstWord = line[:line.find(' ')]
    affectedVar = -1
    counter = -1
    for var in allVars:
        counter += 1
        if var[0][1:] == firstWord:
            affectedVar = counter
    firstSpace = line.find(' ')
    operation = line[firstSpace+1]
    if line[firstSpace + 2] in ['+','-','=']:
        operation += line[firstSpace+2]
    tempOp = line[firstSpace+3:-1].replace(" ","")
    opVars = []
    #Check if there are any operators on the RHS
    otherOp = ''
    if tempOp.find('+') != -1:
        opVars = tempOp.split('+')
        otherOp = '+'
    elif tempOp.find('-') != -1:
        opVars = tempOp.split('-')
        otherOp = '-'
    elif tempOp.find('*') != -1:
        opVars = tempOp.split('*')
        otherOp = '*'
    elif tempOp.find('/') != -1:
        opVars = tempOp.split('/')
        otherOp = '/'
    else:
        #If not, affect the LHS by whatever operator is present

        #If no other value is present, just a simple increment or decrement
        if operation == "++":
            allVars[affectedVar][1] += 1
        if operation == "--":
            allVars[affectedVar][1] -= 1
        #Check to see if the RHS is a variable
        affectingVar = -1
        counter = -1
        for var in allVars:
            counter += 1
            if var[0][1:] == tempOp:
                affectingVar = counter
        #If the left hand side is only one value, adjust the value accordingly
        if affectingVar == -1:
            if operation == "=":
                allVars[affectedVar][1] = tempOp
            if operation == "+=":
                allVars[affectedVar][1] += tempOp
            if operation == "-=":
                allVars[affectedVar][1] -= tempOp
            if operation == "*=":
                allVars[affectedVar][1] *= tempOp
            if operation == "/=":
                allVars[affectedVar][1] /= tempOp
        else:
            if operation == "=":
                allVars[affectedVar][1] = allVars[affectingVar][1]
            if operation == "+=":
                allVars[affectedVar][1] += allVars[affectingVar][1]
            if operation == "-=":
                allVars[affectedVar][1] -= allVars[affectingVar][1]
            if operation == "*=":
                allVars[affectedVar][1] *= allVars[affectingVar][1]
            if operation == "/=":
                allVars[affectedVar][1] /= allVars[affectingVar][1]

    if len(opVars) == 2:
        #Given that the RHS has 2 values, check if either, both, or neither of them are variables
        affectingVar1 = -1
        counter = -1
        for var in allVars:
            counter += 1
            if var[0][1:] == opVars[0]:
                affectingVar1 = counter
        affectingVar2 = -1
        counter = -1
        for var in allVars:
            counter += 1
            if var[0][1:] == opVars[1]:
                affectingVar2 = counter
        lhs = 0
        #if the first value isn't a variable, but just a literal
        if affectingVar1 == -1:
            lhs = opVars[0]
        else:
            lhs = allVars[affectingVar1][1]
        #If the second value isn't a variable
        if affectingVar2 == -1:
            if otherOp == "+":
                lhs += opVars[1]
            if otherOp == "-":
                lhs -= opVars[1]
            if otherOp == "*":
                lhs *= opVars[1]
            if otherOp == "/":
                lhs /= opVars[1]
        else:
            if otherOp == "+":
                lhs += allVars[affectingVar2][1]
            if otherOp == "-":
                lhs -= allVars[affectingVar2][1]
            if otherOp == "*":
                lhs *= allVars[affectingVar2][1]
            if otherOp == "/":
                lhs /= allVars[affectingVar2][1]

        #add the operations completed on the RHS to the LHS with whatever base operation
        if operation == "=":
            allVars[affectedVar][1] = lhs
        if operation == "+=":
            allVars[affectedVar][1] += lhs
        if operation == "-=":
            allVars[affectedVar][1] -= lhs
        if operation == "*=":
            allVars[affectedVar][1] *= lhs
        if operation == "/=":
            allVars[affectedVar][1] /= lhs
    makeJSON(lineNum)
    variableChangeSearch(lineNum+1)


def makeJSON(lineNum):
    global outputString
    global stepCounter
    outputString += '{"'+str(stepCounter)+'": {"lineNumber": '+str(lineNum+1)+','
    for var in allVars:
        outputString += '"'+str(var[0])+'": '+str(var[1])+','
    outputString = outputString[:-1]
    outputString += '}},'
    stepCounter += 1
    return

def untab(line):
    #adjust for tabbing so the start of the line is constant
    while len(line) > 0 and line[0] == '\t' or line[0] == ' ':
        line = line[1:]
    return line

def searcher(line, name, identifier, default, lineNum):
    if line[:len(name)+1] == name+" " and line[len(line)-1] == ';':
        newVarName = line[len(name)+1:line.find(" ",len(name)+1)]
        eqInd = line.find("=")
        if eqInd == -1: #the variable wasn't instantiated
            newVarVal = 0
        else:
            if line[eqInd+1] == ' ':
                newVarVal = line[eqInd+2:-1]
            else:
                newVarVal = line[eqInd+1:-1]
        allVars.append([identifier+newVarName, int(newVarVal)])
        makeJSON(lineNum)
        return True
    return False


startCount = 0
for line in range(len(codeLines)):
    getNextLine(codeLines[line], line)
    if(startLine != -1):
        break
variableChangeSearch(startLine)


    



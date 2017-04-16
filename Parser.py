import re


class Parser:

mainDeclared = False
varType = []
varName = []
varValue = []
arrayIterator = 0
lineNumber = 0
textFile = 'file.txt'

def main(): #iterate through lines of textfile
	
	lineNumber = 0 
	f = open(textFile)

	for i in range(300):
		
		getNextLine(f.next())
	 
f.close()

def getNextLine(line):

    if mainDeclared == False: #is a main fxn declared?
        
		mainDeclaration() #if not, look to see if this line declares it

    else:
        
		searcher(line) #if declared, look to see if anything valuable is on the line

def mainDeclaration(line):

    if mainDeclared == False: #main fxn has not been called yet
   
        if regexSearch = re.compile(r'''(
            #(.*)                           
            ()'static void main') ? 
            )''') == None):
            #if main method not declared
				getNextLine(line)
   
        else:
			#main has been declared
            mainDeclared = True
            searcher(line)

def searcher(line):

    if regexSearch = re.compile(r'''(
         (byte|sbyte|int|uint|short|ushort|long|ulong|float|double|char|decimal) #finds type if mainDeclaration
         )''') == None:
         #nothing declared, search to see if a variable changes
             variableChangeSearch(line)
         
    else:
        
            varType = group()

            regexSearch = re.compile(r'''(
                (\w+)   #find variable name
            )''')

            varName[arrayIterator] = group()

            if (regexSearch = re.compile(r'''(
                (=)?    #does the variable have a value declared?
            )''') == None):
            
                varValue[arrayIterator] = null
                arrayIterator ++

                makeJSON()

            else:

                regexSearch = re.compile(r'''(
                    (\w+)   #find the name
                )''') 

                varValue[arrayIterator] = group()
                arrayIterator ++
                makeJSON()

def variableChangeSearch():

    regexSearch = re.compile(r'''(
        (\w+)   #find the name; group 1
        (\s*)   #0 or more spaces; group 2
        (=|\+\+|--) #equals sign, plus plus, or minus minus; group 3
		(\s*)	#pasrse out the spaces; group 4
		(\w*)	#any variables used in equation; group 5
    )''')

    
    found = False

    i = 0
    while (i < arrayIterator):
   
        if (varName[i] == group(1)):
        
            i = arrayIterator
            found = True
        
        else:
        
            i ++

    if found and group(5) == null:
		
		if group(3) == '++':
			
			if varType[arrayIterator] != char:

				varValue[arrayIterator] ++

		else if group(3) == '--':

			if varType[arrayIterator] != char:

				varValue[arrayIterator] --
		
	else if found:

		regexSearch = re.compile(r'''(
			((\w*)
			\s*
			(\+|-)
			\s*)*
		)''')

		operators = (len(group(0)) - 1) / 2 #number of operators
		varsUsed = group(1)
		opsUsed = group(2)

		j = 0

		while j < len(varsUsed):
			
			if type(varsUsed[j]) == char:

				k = 0
				
				while (k < len(varName)):
   
					if varName[k] == varsUsed[j]:

						varsUsed[j] = varValue[k]
				k ++
			j ++

		result = varsUsed[0]

		j = 0

		while j < len(opsUsed):
			
			if opsUsed[j] == '+':
				
				result = result + varsUsed[j + 1]
			
			else if opsUsed[j] == '-':

				result = result - varsUsed[j + 1]

			j ++

		varValue[arrayIterator] = result
				
def makeJSON():
	
	#takes lineNumber, varType array, varName array, and varValue array and puts into JSON format
	#sends JSON to frontend

				

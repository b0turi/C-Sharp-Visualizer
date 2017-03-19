import re


class Parser:

mainDeclared = False
varType = []
varName = []
varValue = []
arrayIterator = 0
lineNumber = 0

def getNextLine(line):

    if (mainDeclared == false)
    {
        line.mainDeclaration()
    }

    else
    {
        line.searcher()
    }

def mainDeclaration():

    if (mainDeclared == False) #main fxn has not been called yet
    {
        if (regexSearch = re.compile(r'''(
            #(.*)                           #all the stuff before the main method
            ()'static void main') ? #finds the main method
            )''') == None)
            {
                line.getNextLine()
            }
        else
        {
            mainDeclared = True
            line.searcher()
        }
    }

def searcher():

    if (regexSearch = re.compile(r'''(
         (byte|sbyte|int|uint|short|ushort|long|ulong|float|double|char|decimal) #finds type if mainDeclaration
         )''') == None)
         {
             line.variableChangeSearch()
         }
    else
        {
            varType = group()

            regexSearch = re.compile(r'''(
                (\w+)   #find variable name
            )''')

            varName[arrayIterator] = group()

            if (regexSearch = re.compile(r'''(
                (=)?    #does the variable have a value declared?
            )''') == None)
            {
                varValue[arrayIterator] = null
                arrayIterator ++

                line.makeJSON()
            }

            else
            {
                regexSearch = re.compile(r'''(
                    (\w+)   #find the name
                )''') 

                varValue[arrayIterator] = group()
                arrayIterator ++
                line.makeJSON()
            }

        }

def variableChangeSearch():

    regexSearch = re.compile(r'''(
        (\w+)   #find the name
        (\s*)   #0 or more spaces
        (=|\+\+|--) #equals sign, plus plus, or minus minus
    )''')

    
    found = false

    i = 0
    while (i < arrayIterator)
    {
        if (varName[i] == group(1))
        {
            i = arrayIterator
            found = true
        }
        else
        {
            i ++
        }
    }

    if (found)
    {

    }


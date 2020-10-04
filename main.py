import os
from historialLex import regHist
import SQL_CLI
#setSql = []

colorlist = ["blue", "red", "green", "yellow", "orange", "pink"]
tokens = [  ['0', 'create', '1'] ,
            ['1', 'set', '2'] ,        
            ['2', 'idset', '3'] ,      
            ['0', 'load', '4'] ,       
            ['4', 'into', '5'] ,       
            ['5', 'idset', '6'] ,      
            ['6', 'files', '7'] ,      
            ['7', '.aon', '8'] ,       
            ['8', ',', '7'] ,
            ['0', 'use', '1'] ,        
            ['0', 'select', '9'] ,     
            ['9', 'atrbset', '10'] ,   
            ['10', ',', '9'] ,
            ['9', '*', '11'] ,
            ['11', 'where', '12'] ,    
            ['10', 'where', '12'] ,    
            ['12', 'atrbset', '13'] ,  
            ['13', '=', '14'] ,        
            ['13', '!=', '14'] ,       
            ['13', '<', '15'] ,        
            ['13', '>', '15'] ,        
            ['15', '=', '14'] ,        
            ['14', '\\"', '16'] ,      
            ['15', '\\"', '16'] ,      
            ['16', 'cadena', '17'] ,   
            ['17', '\\"', '18'] ,      
            ['14', 'numero', '18'] ,   
            ['14', 'booleano', '18'] , 
            ['15', 'numero', '18'] ,   
            ['15', 'booleano', '18'] , 
            ['18', 'or', '12'] ,       
            ['18', 'and', '12'] ,      
            ['18', 'xor', '12'] ,      
            ['0', 'list', '19'] ,      
            ['19', 'attributes', '3'] ,
            ['0', 'print', '20'] ,     
            ['20', 'in', '21'] ,       
            ['21', 'color', '3'] ,     
            ['0', 'max', '22'] ,       
            ['0', 'min', '22'] ,       
            ['22', 'atrbset', '3'] ,
            ['0', 'sum', '23'] ,
            ['23', 'atrbset', '24'] ,
            ['24', ',', '23'] ,
            ['23', '*', '25'] ,
            ['0', 'count', '23'],
            ['0', 'report', '26'],
            ['26', 'tokens', '27']
        ]

commandSql=[]


def lecturacomando(comando):
    listCommand = []
    listAlternativ = []
    token = ""
    isReserved = True
    readSpace = False
    #leeatrb = False
    countchar = 0
    estadoactual = "0"
    for char in comando:
        countchar += 1
        if isReserved:
            #validar el token y cambiar estado
            if not char.isspace():
                token += char
            #print(searchToken(token.lower()))
            if searchToken(token.lower()):  # valida que el elemento entrante exista en memoria ID - 
                if searchToken(token.lower())=="idset":
                    estadosiguiente = validaTransicion(estadoactual, "idset") #obtiene el estado siguiente del token buscado
                else:
                    estadosiguiente = validaTransicion(estadoactual, token.lower()) #obtiene el estado siguiente del token buscado
                if not estadosiguiente == "None":
                    estadoactual = estadosiguiente
                    listCommand.append(token.lower())
                    #print(token.lower())
                    token = ""
                    if estadoactual == "7":
                        isReserved = False
                    if estadoactual == "23":
                        isReserved = False
            if countchar == len(comando) and token:
                if estadoactual == "2" and listCommand[0] == "create":
                    listCommand.append(token.lower())
                elif estadoactual == "2" and listCommand[0] == "use":
                    #print(token)
                    if searchToken(token.lower())=="idset":
                        listCommand.append(token.lower())
                    else:
                        return False, listCommand
                elif estadoactual == "21" and listCommand[0] == "print":
                    estadoactual = validaTransicion(estadoactual, "color")
                    listCommand.append(token.lower())
                elif estadoactual == "22" and (listCommand[0] == "max" or listCommand[0] == "min"):
                    estadoactual = validaTransicion(estadoactual, "atrbset")
                    listCommand.append(token.lower())
        else:
            if estadoactual == "8" and char == ",":
                #estadoactual = validaTransicion(estadoactual, ".aon") #obtiene el estado siguiente del token buscado
                estadoactual = validaTransicion(estadoactual, char) #obtiene el estado siguiente del token buscado
                if token:
                    #Validar si el archivo es de extension .aon
                    nombre, extension = os.path.splitext(token)
                    if extension == ".aon":
                        listAlternativ.append(token)
                        token = ""
                        listCommand.append(char)
                    else:
                        return False, listCommand
            elif estadoactual == "23" and char == "*":
                estadoactual = validaTransicion(estadoactual, char)
                listAlternativ.append(char)
                listCommand.append(listAlternativ)
            elif estadoactual == "24" and char == ",":
                estadoactual = validaTransicion("23", "atrbset")
                estadoactual = validaTransicion(estadoactual, char)
                if token:
                    listAlternativ.append(token)
                    token = ""
                    listCommand.append(char)
            elif not char.isspace():
                token += char
                if estadoactual == "7":
                    estadoactual = "8"
                elif estadoactual == "23":
                    estadoactual = "24"
            else:
                if token:
                    if estadoactual == "8":
                        #Validar si el archivo es de extension .aon
                        nombre, extension = os.path.splitext(token)
                        if extension == ".aon":
                            listAlternativ.append(token)
                            token = ""
                            isReserved = True
                        else:
                            return False, listCommand
                    if estadoactual == "24":
                        listAlternativ.append(token)
                        token = ""
                        isReserved = True
            if countchar == len(comando) and token:
                if estadoactual == "8":
                    nombre, extension = os.path.splitext(token)
                    if extension == ".aon":
                        listAlternativ.append(token)
                        listCommand.append(listAlternativ)
                    else:
                        return False, listCommand
                if estadoactual == "24":
                    listAlternativ.append(token)
                    listCommand.append(listAlternativ)
    if listCommand:
        return True, listCommand
    else:
        return False, listCommand

def validaTransicion(estadoA, tokenlect):
    for tk in tokens:
        if tk[0] == estadoA and tk[1] == tokenlect:
            return tk[2]
    return "None"

def searchToken(tokn):
    for tk in tokens:
        if tk[1] == tokn:
            return "idpropio"
    for tk in SQL_CLI.getListaSets():
        if tk == tokn:
            return "idset"
    return ""

def init(elcomando):
    isComand, listCommand = lecturacomando(elcomando)
    #isComand, listCommand = lecturacomando("Loadinto carros")
    if isComand:
        #print("\n ------ ", listCommand, " ------ ")
        if listCommand[0] == "create":
            if len(listCommand) == 3:
                regHist(listCommand)
                SQL_CLI.createSet(listCommand[2].lower())
            else:
                print("Error de comando")
            #print("Sets registrados: ",SQL_CLI.getListaSets())
        elif listCommand[0] == "load":
            #print(SQL_CLI.getListaSets())
            tam = len(listCommand) - 1
            if len(listCommand) >= 5:
                try:
                    n, ext = os.path.splitext(listCommand[tam][0])
                    if ext == ".aon":
                        regHist(listCommand)
                        SQL_CLI.loadAon(listCommand[2], listCommand[tam])
                    else:
                        print("Error de comando")
                except IndexError:
                    print("Error de comando")
            else:
                print("Error de comando")
        elif listCommand[0] == "use":
            if len(listCommand) == 3:
                if SQL_CLI.isSetonDB(listCommand[2]):
                    regHist(listCommand)
                    SQL_CLI.setToUse(listCommand[2])
                else:
                    SQL_CLI.setToUse("None")
                    print("El set " + listCommand[2] +" no posee registros para ser utilizado")
            else:
                print("Error de comando")
        elif listCommand[0] == "list":
            if len(listCommand) == 2:
                if SQL_CLI.isSetUse():
                    regHist(listCommand)
                    SQL_CLI.showAttrb()
                else:
                    print("No se ha establecido el set a usar")
            else:
                print("Error de comando")
        elif listCommand[0] == "print":
            if len(listCommand) == 3:
                if colorlist.__contains__(listCommand[2]):
                    regHist(listCommand)
                    SQL_CLI.setPrintInColor(listCommand[2])
                else:
                    print("Error de color")
            else:
                print("Error de comando")
        elif listCommand[0] == "max":
            if len(listCommand) == 2:
                if SQL_CLI.isSetUse():
                    if SQL_CLI.getKeysOfSet().__contains__(listCommand[1]):
                        regHist(listCommand)
                        SQL_CLI.searchMax(listCommand[1])
                    else:
                        print("Error, atributo no encontrado")
                else:
                    print("No se ha definido el set a usar")
            else:
                print("Error de comando")
        elif listCommand[0] == "min":
            if len(listCommand) == 2:
                if SQL_CLI.isSetUse():
                    if SQL_CLI.getKeysOfSet().__contains__(listCommand[1]):
                        regHist(listCommand)
                        SQL_CLI.searchMin(listCommand[1])
                    else:
                        print("Error, atributo no encontrado")
                else:
                    print("No se ha definido el set a usar")
            else:
                print("Error de comando")
        elif listCommand[0] == "sum":
            if len(listCommand) >= 2:
                if SQL_CLI.isSetUse():
                    tm = len(listCommand) - 1
                    try:
                        if listCommand[1][0] == "*" and SQL_CLI.getKeysOfSet():
                            regHist(listCommand)
                            SQL_CLI.doSum(listCommand[1])
                        else:
                            isOK = True
                            for at in listCommand[tm]:
                                if not SQL_CLI.getKeysOfSet().__contains__(at):
                                    isOK = False
                            if isOK:
                                regHist(listCommand)
                                SQL_CLI.doSum(listCommand[tm])
                            else:
                                print("Error, atributo no encontrado")
                    except:
                        print("Error de comando")
                else:
                    print("No se ha definido el set a usar")
            else:
                print("Error de comando")
        elif listCommand[0] == "count":
            if len(listCommand) >= 2:
                if SQL_CLI.isSetUse():
                    tm = len(listCommand) - 1
                    try:
                        if listCommand[1][0] == "*" and SQL_CLI.getKeysOfSet():
                            regHist(listCommand)
                            SQL_CLI.doCount(listCommand[1])
                        else:
                            isOK = True
                            for at in listCommand[tm]:
                                if not SQL_CLI.getKeysOfSet().__contains__(at):
                                    isOK = False
                            if isOK:
                                regHist(listCommand)
                                SQL_CLI.doCount(listCommand[tm])
                            else:
                                print("Error, atributo no encontrado")
                    except:
                        print("Error de comando")
                else:
                    print("No se ha definido el set a usar")
            else:
                print("Error de comando")
        elif listCommand[0] == "report":
            if len(listCommand) == 2:
                regHist(listCommand)
                SQL_CLI.reportTokens()
            else:
                print("Error de comando")
    else:
        print("Error de comando")
    print()
    
def toReportHtml():
    pass

def elmetodo():
    init("CREATE SET carros")
    init("CREATE SET palabras")
    #init("LOAD INTO carros files archivo.aon, archivo2.aon, archivo3.aon")
    init("LOAD INTO carros files archivo.aon")
    #init("LOAD INTO carros files archivo2.aon, load.aon")
    #init("LOAD INTO palabras files archivo.aon")
    init("LOAD INTO palabras files archivo2.aon")
    init("use set carros")
    #init("use set palabras")
    init("print in orange")
    init("min precio")
    init("MAX precio")
    init("list attributes")
    #init("sum numero, cadena")
    #init("sum numero")
    init("sum *")
    init("count precio, descripcion")
    #init("count precio")
    #init("count *")
    init("print in yellow")
    init("report tokens")

elmetodo()
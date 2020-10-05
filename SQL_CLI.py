from colorama import init, Fore
import time
import json
import os
import reporte
import historialLex
#import reporte
from AONanalyzer import analizadorAON

setSql = []
dbSets = {}
setUse = []
colorUse = ["green"]
boolReport = False
eltxt = ""

init() # Funcion que inicia la funcion de print en color
print(Fore.GREEN)

def setPrintInColor(colorToUse):
    colorUse.clear()
    colorUse.append(colorToUse)
    if colorUse[0] == "blue":
        print(Fore.BLUE)
    elif colorUse[0] == "red":
        print(Fore.RED)
    elif colorUse[0] == "green":
        print(Fore.GREEN)
    elif colorUse[0] == "yellow":
        print(Fore.YELLOW)
    elif colorUse[0] == "orange":
        print(Fore.LIGHTRED_EX)
    elif colorUse[0] == "pink":
        print(Fore.MAGENTA)
    print("Se ha modificiado el color de fuente")

def getSource(): #Obtiene la ruta del script
    ruta = os.path.dirname(os.path.abspath(__file__))
    return ruta

def dbempty(): #Evalua si la db esta vacia
    if len(dbSets) == 0:
        return False
    else:
        return True

def getListaSets(): #Devuelve la lista de sets "creados"
    return setSql

def isSetUse(): #Devuelve True/False si hay un set en uso
    if setUse:
        return True
    else:
        return False

def setToUse(toUse): #Modifica el set a usar  //////////////
    if setUse:
        if toUse == "None":
            setUse.clear()
        else:
            setUse.clear()
            setUse.append(toUse)
            print("Se está usando el set ", toUse.upper())
    else:
        if toUse == "None":
            setUse.clear()
        else:
            setUse.append(toUse)
            print("Se está usando el set ", toUse.upper())

def getKeysOfSet(): #Devuelve las keys de un set
    try:
        return dbSets[setUse[0]][0].keys()
    except KeyError:
        print("El set no posee registros")
        return

def createSet(nameOfSet): #Añade el set a la lista de sets /////////
    if not setSql.__contains__(nameOfSet):
        print("El set ", nameOfSet, " se ha creado exitosamente")
        setSql.append(nameOfSet)
    else:
        print("El set ", nameOfSet, " ya está registrado")
        print()

def isSetonDB(toUse): #Valida si un set tiene registros en la db
    if dbSets.keys().__contains__(toUse):
        return True
    else:
        return False

def loadAon(setload, listf): #Carga los archivos a la db ////////
    listForDict = []
    for f in listf:
        fileOn = getSource() + "/" + f
        if os.path.isfile(fileOn):
            print(" -- Fichero " + f +" encontrado -- ")
            listaT = analizadorAON(f)
            if listaT:
                listForDict.extend(listaT.copy())
        else:
            print(" -- Fichero " + f +" no encontrado -- ")

    if listForDict:
        if dbSets.keys().__contains__(setload):
            dbSets[setload].extend(listForDict)
        else:
            dcT = {setload : listForDict}
            dbSets.update(dcT)

def showAttrb(): #Muestra los atributos del set   /////////
    listAtrb = dbSets[setUse[0]]
    if boolReport:
        pass
    else:
        print("Set en uso: " , str(setUse[0].upper()))
        for atrb in listAtrb[0].keys():
            print("                 - " , str(atrb))

def searchMin(attribUse):
    listT = dbSets[setUse[0]]
    try:
        minim = []
        for r in listT:
            #print(r)
            if minim:
                if minim[0] > r[attribUse]:
                    minim.clear()
                    minim.append(r[attribUse])
            else:
                minim.append(r[attribUse])
        print("El valor minimo para ", str(attribUse.upper()), " del set: ", setUse[0].upper(), " es: ", minim[0])
    except:
        print("Error en busqueda minimo")

def searchMax(attribUse):
    listT = dbSets[setUse[0]]
    try:
        maxim = []
        for r in listT:
            #print(r)
            if maxim:
                if maxim[0] < r[attribUse]:
                    maxim.clear()
                    maxim.append(r[attribUse])
            else:
                maxim.append(r[attribUse])
        print("El valor maximo para ", str(attribUse.upper()), " del set: ", setUse[0].upper(), " es: ", maxim[0])
    except:
        print("Error en busqueda maximo")

def getRegisList():
    return dbSets[setUse[0]]

def doSum(lAtrib):
    listOfResults = []
    if lAtrib[0] == "*":
        lAtrib = list(getKeysOfSet())
    for req in lAtrib:
        rl = getRegisList()
        #print("lista reg ", rl[0])
        if esNumero(rl[0][req]):
            suma = 0
            for r in rl:
                try:
                    suma = suma + r[req]
                except:
                    suma = suma + 0
            ltmp = [req, suma]
            listOfResults.append(ltmp)
        else:
            ltmp = [req, "NO NUMERICO"]
            listOfResults.append(ltmp)
    print("\n ---------- RESULTS ----------")
    for res in listOfResults:
        print(res[0].upper(), ": ", res[1])

def doCount(lAtrib):
    listOfResults = []
    if lAtrib[0] == "*":
        lAtrib = list(getKeysOfSet())
    for req in lAtrib:
        rl = getRegisList()
        count = 0
        for r in rl:
            try:
                if r[req] or r[req] == False:
                    count += 1
            except:
                count += 0
        ltmp = [req, count]
        listOfResults.append(ltmp)
    print("\n ---------- COUNT ----------")
    for res in listOfResults:
        print(res[0].upper(), ": ", res[1])

def esNumero(val):
    v = str(val)
    for n in v:
        if not n.isdigit():
            if not n == ".":
                #print(n)
                return False
    return True

def reportTokens():
    reporte.generaHtml("TOKENS", ["Lexema", "Id Token", "Descripción"], historialLex.getHisto())
    #historialLex.muestraHist()

def readSiQLScript(scpt):
    fileOn = getSource() + "/" + scpt
    if os.path.isfile(fileOn):
        listT = []
        print(" -- Fichero " + scpt +" encontrado -- ")
        file = open(fileOn, "r")
        com = ""
        for li in file:
            for ch in li.rstrip():
                if not ch == ";":
                    com += ch
                else:
                    if com:
                        listT.append(com)
                    com = ""
        return listT
    else:
        print(" -- Fichero " + f +" no encontrado -- ")

def selectReq(latr, conditions):
    #print("si llega")
    if "*" in latr:
        if not conditions:
            atr = getKeysOfSet()
            setU = dbSets[setUse[0]]
            listResult = []
            for reg in setU:
                ltmp = []
                for at in atr:
                    try:
                        ltmp.append(reg[at])
                    except KeyError:
                        ltmp.append("Null")
                listResult.append(ltmp.copy())
            sep = separadorvertical(atr)
            print(sep)
            line = ""
            for k in atr:
                line += (aniadeespacio(k.upper()) + "||")
            print(line)
            print(sep)
            for res in listResult:
                line = ""
                for reg in res:
                    line += (aniadeespacio(reg) + "||")
                print(line)
                print(sep)
        else:
            pass
        #dar formato al resultado
    else:
        pass

def separadorvertical(n):
    try:
        if n == "*":
            n = ["*", "*", "*", "*"]
    except:
        pass
    sep = ""
    init = True
    for i in range(0, len(n)):
        if init:   
            sep = "--------------------------------||"
            init = False
        else:
            sep = sep + "--------------------------------||"
    return sep

def aniadeespacio(elemento):
    elem = str(elemento)
    k = 32
    k = k - len(elem)
    spaces = ""
    for i in range(0, k):
        spaces = spaces + " "
    elem = elem + spaces
    return elem

def showWithFormat():
    pass

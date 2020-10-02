import time
import json
import os
#import reporte
from AONanalyzer import analizadorAON

setSql = []
dbSets = {}
setUse = ""

def getSource():
    ruta = os.path.dirname(os.path.abspath(__file__))
    return ruta

def dbempty():
    if len(dbSets) == 0:
        return False
    else:
        return True

def getListaSets():
    return setSql

def isSetUse():
    if setUse:
        return True, setUse
    else:
        return False, setUse

def getKeysOfSet(setInUse):
    try:
        return dbSets[setInUse][0].keys()
    except KeyError:
        print("El set no posee registros")

def createSet(nameOfSet):
    if not setSql.__contains__(nameOfSet):
        print("El set ", nameOfSet, " se ha creado exitosamente")
        setSql.append(nameOfSet)
    else:
        print("El set ", nameOfSet, " ya está registrado")
        print()


def loadAon(setload, listf):
    listForDict = []
    for f in listf:
        #print(" -- Si llega la lista de archivos -- ", f)
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
        #dbSets.update(dcT)
        #print("From " + setload + ":")
        #for K in dbSets.keys():
        #    print(K)
        #    for elem in dbSets[K]:
        #        print(elem)

        


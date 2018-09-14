# -*- coding: utf-8 -*-
"""
Created on Wed Sep  3 15:30:15 2018
Transform rel-data format into openKE format, see
https://github.com/phohenecker/rel-data#data-format
https://github.com/thunlp/OpenKE

Returns OpenKE files:   relation2id.txt, entity2id, train2id.txt, valid2id.txt,  test2id.txt, type_constrain.txt. 
Literals omitted  (not clear if it makes senses with classical link prediction models, and dbpedia cases are empty).


@author: Emilio Serrano and Thomas Lukasiewicz
"""




from relData2OpenKETools import *
from sample2EntitiesAndTriples import *
from iDManager import *
import random  

from os import listdir
from os.path import isfile, join
import os


#path with rel2data dev,test, and train directories
pathForKB="C:/media/datasets oxford/Patrick 2018/dbpedia-50" #"/home/serrano/dbpedia-5000"
#outputfolder
outputPath="C:/media/datasets oxford/Patrick 2018/relData2OpenKEOuput" #/home/serrano/dbpediaToOpenKE
#outputPath="C:/media/datasets oxford/Patrick 2018/claros-5000-OKE" #/home/serrano/dbpediaToOpenKE


#random seed to shuffle validation and testing data
seed=123
#partition of training, validation, testing considering infereable data (60%,20%,20%)
partitions=[0.6,0.2,0.2]


#list of subfolders to consider in the path
foldersInPathForKB= [pathForKB + "/train/", pathForKB + "/dev/", pathForKB + "/test/" ] #pathForKB + "/test/" and to add train 

#Aux files generated with IDs depending on the file name, all samples for the folders gien in foldersInPathForKB are readed
def generateAuxFiles():
    print("Writing aux files to from following folders:" + str(foldersInPathForKB) + "...")
    
    #KB samples IDs with the path they are, e.g. [...[['5500', 'C:/media/datasets oxford/Patrick 2018/dbpedia-5000/test']...]
    filesIDs= getSamplesIDsInSeveralFolders(foldersInPathForKB)        
    #deal with one sample given the id and path
    s2e=sample2EntitiesAndTriples(filesIDs[0][0], filesIDs[0][1])
    #relations and classes are the same for the whole KB, only generated once
    writeToFile(s2e.relations, outputPath + "/relationsAux.txt" ,False) 
    writeToFile(s2e.classes, outputPath + "/entitiesAux.txt" ,False)
    #entities added after the classes
    writeToFile(s2e.entities, outputPath + "/entitiesAux.txt" ,True) 
    
    #first triples generated, the rest will be added in the file
    writeToFile(s2e.triples, outputPath + "/triplesAux.txt" ,False)         
    writeToFile(s2e.triplesInfereable, outputPath + "/triplesInfereableAux.txt" ,False)   
    #iterate skipping first file    
    iterfiles = iter(filesIDs)
    next(iterfiles)
    for fID in iterfiles:        
        s2e=sample2EntitiesAndTriples(fID[0], fID[1])
        writeToFile(s2e.entities, outputPath + "/entitiesAux.txt" ,True) 
        writeToFile(s2e.triples, outputPath + "/triplesAux.txt" ,True) 
        writeToFile(s2e.triplesInfereable, outputPath + "/triplesInfereableAux.txt" ,True)   

    
    print("...OK")
        

def generateIDMaps():
    print("Removing repetitions in entities IDs and assigning global IDs for entities and classes in all files...")    
    idm=iDManager(outputPath)
    idm.assingEntitiesID(outputPath + "/entitiesAux.txt")
    print("...OK")

    return idm
    


def generateOpenKEFiles(myiDManager):
    print("Generating final OpenKE files...")    
    #relations only need to change order of id and name
    relations = fileAsList(outputPath + "/relationsAux.txt")    
    relations2=[]
    for r in relations:    
        r2=r.split()   
        relations2.append([r2[1],r2[0]])    
    writeToFile(relations2, outputPath + "/relation2id.txt" ,False,True)    
    

    #entities need to change order of id and name, and introduce the new id
    entities = fileAsList(outputPath + "/entitiesAux.txt")    
    entities2=[]
    for e in entities:    
        e2=e.split()   
        entities2.append([e2[1],idm.getNewIDFromEntityName(e2[1])])    
    writeToFile(entities2, outputPath + "/entity2id.txt" ,False,True)       
    
          
    #train, validation, and testing. Aux are already in e1,e2, relation order... only the ids have to change
    #80% of infereable are added in train, 20% validation, 20% in testing AFTER SHUFFLE
    triples = fileAsList(outputPath + "/triplesAux.txt")     
    triples2=[]
    for t in triples:    
        t2=t.split()   
        triples2.append([idm.getNewIDFromOldID(t2[0]), idm.getNewIDFromOldID(t2[1]), t2[2]])    
    #triples2 list has to be completed with infereable triples
 
    triplesInfereable = fileAsList(outputPath + "/triplesInfereableAux.txt")        
    random.seed(seed)                        
    random.shuffle(triplesInfereable)
    indexForValidation = int(round(len(triplesInfereable)*partitions[0])) #validation data start after 60% of the list
    indexForTesting= int(round(len(triplesInfereable)*( partitions[0] +  partitions[1]))) #testing data start after 80% of the list

    for i in range(0,indexForValidation):    
        t2=triplesInfereable[i].split()   
        #print(str(i) + " infereable triple for training ")
        triples2.append([idm.getNewIDFromOldID(t2[0]), idm.getNewIDFromOldID(t2[1]), t2[2]])         
    writeToFile(triples2, outputPath + "/train2id.txt" ,False,True)  
    
    triples2=[] #empty list for validation
    for i in range(indexForValidation,indexForTesting):    
        t2=triplesInfereable[i].split()   
        #print(str(i) + " infereable triple for validation ")
        triples2.append([idm.getNewIDFromOldID(t2[0]), idm.getNewIDFromOldID(t2[1]), t2[2]])         
    writeToFile(triples2, outputPath + "/valid2id.txt" ,False,True)  
    
    triples2=[]
    for i in range(indexForTesting,len(triplesInfereable)):    
        t2=triplesInfereable[i].split()   
        #print(str(i) + " infereable triple for testing ")
        triples2.append([idm.getNewIDFromOldID(t2[0]), idm.getNewIDFromOldID(t2[1]), t2[2]])         
    writeToFile(triples2, outputPath + "/test2id.txt" ,False,True)  
    
    print("...OK")


def removeAuxFiles():
    print("Removing aux files...")
    os.remove( outputPath + "/relationsAux.txt")
    os.remove( outputPath + "/entitiesAux.txt")
    os.remove( outputPath + "/triplesAux.txt")
    os.remove( outputPath + "/triplesInfereableAux.txt")
    print("...OK")
    
    
#check repetitiosna in triples of train2id and remove overlappings with valid2id andtest2id
#generateOpenKEFiles() is needed first so global identifiers are alreay there
def checkRepetitionsInOpenKEFilesAndRemoveOverlappings():
    print("Checking repetitions in triples and overlapping with validation and testing...")
    
    trainFile=outputPath + "/train2id.txt"
    valFile=outputPath + "/valid2id.txt"
    testFile=outputPath + "/test2id.txt"
    #load list  
    listTrain=fileAsList(trainFile) 
    listVal=fileAsList(valFile)
    listTest=fileAsList(testFile)
    #remove first element  remove the first element with pop because it contains the number of triples
    listTrain.pop(0)
    listVal.pop(0)
    listTest.pop(0)
    
    
    #remove repetitions in lists, the order is lost  
    listTrain=list(set(listTrain))
    listVal=list(set(listVal))
    listTest=list(set(listTest))
    
        

    #check val and test triples in train to remove them
    overlapping= len(list(listTrain+listVal+listTest)) - len(list(set(listTrain+listVal+listTest)))
    if(overlapping>0):
        print("\t..." + str(overlapping) + " relations are repeated in training, validation, and testing! (wait for removal)")    
        for tt in listTrain:
            if tt in listVal:
                listVal.remove(tt)
    
        for tt in listTrain:
            if tt in listTest:
                listTest.remove(tt)
    
    #write files again
    writeToFile(listTrain,trainFile ,False,True,False)    
    writeToFile(listVal, valFile ,False,True,False)    
    writeToFile(listTest, testFile,False,True,False)    
    
    print("...OK")  
    
    
if __name__ == '__main__':
    generateAuxFiles()
    idm= generateIDMaps()
    generateOpenKEFiles(idm)    
    checkRepetitionsInOpenKEFilesAndRemoveOverlappings()
    writeConstraintFiles(outputPath)
    removeAuxFiles()    
    
    #code to check repetition in training
    #checkRepetitionsInOpenKEFile(outputPath + "/train2id.txt")
    #checkRepetitionsInOpenKEFile(outputPath + "/valid2id.txt")
    #checkRepetitionsInOpenKEFile(outputPath + "/test2id.txt")
 


"""
Created on Thu Sep  6 15:15:40 2018

Class to deal with repeated entities in aux files obtained by sample2EntitiesAndTriples and assigning a numeric id from 0..entityNumber

@author: Emilio Serrano and Thomas Lukasiewicz
"""
import json

 
class iDManager:
    
    def __init__(self, outputPath):
 
    
        self.IDsToName={}  
        self.nameToNewID={}
        self.numberOfRepetions=0
        

        self.outputPath =outputPath#to store dictionaries
     
    #to remove repetition preserving order
    def unique(self, sequence):
        seen = set()
        return [x for x in sequence if not (x in seen or seen.add(x))]
            
    # load dictionaries if previously calculated with assingEntitiesID
    def loadDictionariesFromFiles(self):
        with open(self.outputPath + "/nameToNewID.json") as f:
             self.nameToNewID  = json.load(f)
        with open(self.outputPath + "/IDsToName.json") as f:
             self.IDsToName  = json.load(f)
             
             
        
    #check repetitions in entities id from triples aux generated in relData2OpenKE and obtain maps to transform in new IDs
    def assingEntitiesID(self,pathOfEntitiesAux):
        list1=[]
        with open(pathOfEntitiesAux) as f:
            list1 = f.read().splitlines()         
    

        namesWithRepetitions=[]
        for entity in list1: #first position ID, second position Name
            e=entity.split()        
            self.IDsToName[e[0]]=e[1]
            namesWithRepetitions.append(e[1])
            
        
        #list with entity names without repetitions and map with global index
        #namesWithRepetitions= list(self.IDsToName.values())
        namesWithoutRepetitions= list(self.unique(namesWithRepetitions))
        self.numberOfRepetions= len(namesWithRepetitions)- len(namesWithoutRepetitions)        
        for i in range(0, len(namesWithoutRepetitions)):
            self.nameToNewID[namesWithoutRepetitions[i]]= str(i)
            
        #store dictionaries
        #self.saveDictionaries()
 
    
    def saveDictionaries(self):
        data = json.dumps(self.nameToNewID)
        f = open(self.outputPath + "/nameToNewID.json", "wb")        
        #use the following if enconding problems
        #f = open(self.outputPath + "/nameToNewID.json", "w",  encoding="utf8")        
        f.write(data)
        f.close()
        data = json.dumps(self.IDsToName)
        f = open(self.outputPath + "/IDsToName.json", "wb")
        #f = open(self.outputPath + "/IDsToName.json", "w", encoding="utf8")        
        f.write(data)
        f.close()

             
                         
    
    #obtain the new ID from the old one
    def getNewIDFromOldID(self, oldID):
        return self.nameToNewID[self.IDsToName[oldID]]
        
    #obtain the new ID from the old one
    def getNewIDFromEntityName(self, name):
        return self.nameToNewID[name]


    
#SOME TESTING CODE...            
#idm=iDManager("C:/media/datasets oxford/Patrick 2018/toOpenKE")
#idm.assingEntitiesID("C:/media/datasets oxford/Patrick 2018/toOpenKE/entitiesAux.txt")
#idm.saveDictionaries()
#print("Repeated entities IDs: " + str(idm.numberOfRepetions))
#idm.loadDictionariesFromFiles()
#print(idm.nameToNewID)
#print(idm.getNewIDFromEntityName("http://dbpedia.org/resource/Evangeline_Lilly"))

 

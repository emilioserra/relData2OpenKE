# -*- coding: utf-8 -*-
"""
Created on Thu Sep  6 15:15:40 2018

Class to deal with just one sample of rel-data format.
It add the sample id (e.g. 4000_) to the individuals ids (classes and relations has the same id across all KG files in rel-data)
Both class belonging and relations, both inference and prediction data, are added as triples in a triples list
Results in properties: entities, classes, relations, and triples (and tiplesInfereable). 
They can be stored in an aux file for further treatment sucha as  removing repeated entities, assigning global id from 0...number of entitityes



@author: Emilio Serrano and Thomas Lukasiewicz
"""

 


class sample2EntitiesAndTriples:
    
    def __init__(self, sampleID, pathFile):
        self.sampleID= sampleID
        self.pathFile=pathFile
        
        
        
        #list with entities and ids, triples, and classes and ids
        self.entities=[]
        self.classes=[]
        self.relations=[]
        self.triples=[]
        self.triplesInfereable=[] #infereable triples which can be used for testing
        self.classBelongingId=0 #id for the relation class belonging

                
        #methods to load IDS for relations, classes and entities
        self.loadRelations()
        self.loadClasses() 
        self.loadEntities()
        
        
        
        
        #load triples and belonging as tirples
        self.loadTriples()    
        self.loadBelonging()
        
    
    #besides loading realtions of rel-data, add a last and extra relation for class belonging
    def loadRelations(self):
        file=self.pathFile + "/" + self.sampleID + ".relations"
        self.relations = self.fileAsList(file,  "")     
        self.classBelongingId= str(len(self.relations))
        self.relations.append([self.classBelongingId,"ClassBelonging"])
    
    def loadClasses(self):
 
        file=self.pathFile + "/" + self.sampleID + ".classes"
        self.classes = self.fileAsList(file, "")
        
    def loadEntities(self):
        file=self.pathFile + "/" + self.sampleID + ".individuals"
        self.entities = self.fileAsList(file, self.sampleID + "_")                    
    
    #load triples from .relations.data, .relations.data.pred, .relations.data.inf
    #add the file in the individuals id
    def loadTriples(self):
        file=self.pathFile + "/" + self.sampleID + ".relations.data"
        self.addTriples(file,self.sampleID + "_")
        file=self.pathFile + "/" + self.sampleID + ".relations.data.pred"
        self.addTriples(file,self.sampleID + "_")
        file=self.pathFile + "/" + self.sampleID + ".relations.data.inf"
        self.addTriples(file, self.sampleID + "_", True)

    #load "belong to class" triples from classes.data, .classes.data.pred and .classes.data.inf
    #those are added in the triple list, the class id does not contain a file prefix since they are shared among all data samples
    def loadBelonging(self):
        file=self.pathFile + "/" + self.sampleID + ".classes.data"
        self.addBelonging(file,self.sampleID + "_")
        file=self.pathFile + "/" + self.sampleID + ".classes.data.pred"
        self.addBelonging(file,self.sampleID + "_")
        file=self.pathFile + "/" + self.sampleID + ".classes.data.inf"
        self.addBelonging(file, self.sampleID + "_", True)
                        
    
    #auxiliar for loadRelations, load loadClasses, and loadEntities
    #read a file and return a list, a prefix por the first position (id) can be included
    #the prefix is important to use/recover a global identifier for an entitiy in the whole Knowledge graph of rel-data format
    def fileAsList(self, file, prefix ):    
        with open(file) as f:
            list1 = f.read().splitlines()
        list2=[] 
        for e in list1:        
            e2 = e.split()
            if prefix != "":
                e2[0]= prefix + e2[0]
            list2.append(e2)
        return(list2)
        
    
    #auxiliar function for loadTriples
    # extend triple list of list with triples from files such as ".relations.data, .relations.data.pred, .relations.data.inf
    #only consider positive triples 
    # rel-data format <+|-> <SUBJECT-ID> <PREDICATE-ID> <OBJECT-ID> to OpenKE format  e1, e2, rel
    #add prefix of file in entitities
    #if inferable, they are stored in the list of tiplesInfereable
    def addTriples(self, file, prefix, infereable=False):   
        
        tripleList = self.triples
        if infereable:
            tripleList = self.triplesInfereable
        with open(file) as f:
            list1 = f.read().splitlines()    
        for t in list1:  
            triple=t.split()   
            if(triple[0]=='+'): #only positive triples                
                tripleList.append([prefix + triple[1], prefix + triple[3],triple[2]])
                
                
                
    #auxiliar function for adding to belonging to triples
    #add triples in the form of: entity id with prefix, class id without prefix (shared for all files), and id of the belonging relation
    #if inferable, they are stored in the list of tiplesInfereable

    def addBelonging(self, file, prefix, infereable=False):   
        belongings=  self.fileAsList(file,"")
        tripleList = self.triples
        if infereable:
            tripleList = self.triplesInfereable
        for i, entity in enumerate(belongings):
            for j, classBelonging in enumerate(entity):
                #print("entity "+ str(i) + "," + str(j) + ":" + classBelonging )
                if classBelonging=="1":
                   tripleList.append([prefix + str(i), str(j), self.classBelongingId])

        
        
        
   
    

        

        
        
        

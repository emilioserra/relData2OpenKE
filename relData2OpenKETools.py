# -*- coding: utf-8 -*-
"""
Created on Wed Sep  3 15:30:15 2018
auxiliar functions to transform rel-data format into openKE format
 
@author: Emilio Serrano
"""

 

from os import listdir
from os.path import isfile, join


 

#write a list of list in a file (add true to add instead of remove file, number of elements TRue si se quiere añadir número de elementos a copiar)
def writeToFile(listData,outputFile,add, numberOfElements=False):
    addOrWrite='w'
    if add==True:
        addOrWrite='a'    
    with open(outputFile, addOrWrite) as f:
        if numberOfElements:
            f.write( str(len(listData)) + '\n') 
        for line in listData:
            f.write(" ".join(line) + '\n') #write rows separated with space
                
                
 #f.write(str(len(listData)) + '\n') #write the number of entities id/relations id/ triples stored
 
 
 #get a list with the samples of KB IDs, such as 0000-5000, in  a rel-data folder, such as ./train
def getSamplesIDs(pathForKB):
    #all files
    files1 = [f for f in listdir(pathForKB) if isfile(join(pathForKB, f))]
    #remove from dot
    files2=[]
    for f in files1:
        files2.append(f[0:f.index(".")])
    #remove repetitions and order
    files3= sorted(list(set(files2)))
    return files3


 #get a single list of lists [... [sample of KB IDs such as 5000, path of the sample], ...]
 #
def getSamplesIDsInSeveralFolders(foldersInPathForKB):
    #all files
    files=[]
    for fip in foldersInPathForKB:
        fileInFolder= getSamplesIDs(fip)
        for f in fileInFolder:
            files.append([f,fip])
    return files

#list of line of file per element
def fileAsList(filePath):    
    with open(filePath) as f:
         list1 = f.read().splitlines()
    return list1
 
    
    
    


 
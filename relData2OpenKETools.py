# -*- coding: utf-8 -*-
"""
Created on Wed Sep  3 15:30:15 2018
auxiliar functions to transform rel-data format into openKE format
 
@author: Emilio Serrano and Thomas Lukasiewicz
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
 
    
    
    
#obtain constraint.txt, uses n-n.py code by OpenKE
#uses the final files obtained for OpenKE, train2id, valid2id, test2id...

def writeConstraintFiles(outuputPath):
   print("Generating openKE constraint files...")
   lef = {}
   rig = {}
   rellef = {}
   relrig = {}

   triple = open(outuputPath + "/train2id.txt", "r")
   valid = open(outuputPath + "/valid2id.txt", "r")
   test = open(outuputPath + "/test2id.txt", "r")

   tot = (int)(triple.readline())
   for i in range(tot):
      content = triple.readline()
      h,t,r = content.strip().split()
      if not (h,r) in lef:
         lef[(h,r)] = []
      if not (r,t) in rig:
         rig[(r,t)] = []
      lef[(h,r)].append(t)
      rig[(r,t)].append(h)
      if not r in rellef:
         rellef[r] = {}
      if not r in relrig:
         relrig[r] = {}
      rellef[r][h] = 1
      relrig[r][t] = 1

   tot = (int)(valid.readline())
   for i in range(tot):
      content = valid.readline()
      h,t,r = content.strip().split()
      if not (h,r) in lef:
         lef[(h,r)] = []
      if not (r,t) in rig:
         rig[(r,t)] = []
      lef[(h,r)].append(t)
      rig[(r,t)].append(h)
      if not r in rellef:
         rellef[r] = {}
      if not r in relrig:
         relrig[r] = {}
      rellef[r][h] = 1
      relrig[r][t] = 1

   tot = (int)(test.readline())
   for i in range(tot):
      content = test.readline()
      h,t,r = content.strip().split()
      if not (h,r) in lef:
         lef[(h,r)] = []
      if not (r,t) in rig:
         rig[(r,t)] = []
      lef[(h,r)].append(t)
      rig[(r,t)].append(h)
      if not r in rellef:
         rellef[r] = {}
      if not r in relrig:
         relrig[r] = {}
      rellef[r][h] = 1
      relrig[r][t] = 1

   test.close()
   valid.close()
   triple.close()

   f = open(outuputPath + "/type_constrain.txt", "w")
   f.write("%d\n"%(len(rellef)))
   for i in rellef:
      f.write("%s\t%d"%(i,len(rellef[i])))
      for j in rellef[i]:
         f.write("\t%s"%(j))
      f.write("\n")
      f.write("%s\t%d"%(i,len(relrig[i])))
      for j in relrig[i]:
         f.write("\t%s"%(j))
      f.write("\n")
   f.close()

   rellef = {}
   totlef = {}
   relrig = {}
   totrig = {}

   for i in lef:
      if not i[1] in rellef:
         rellef[i[1]] = 0
         totlef[i[1]] = 0
      rellef[i[1]] += len(lef[i])
      totlef[i[1]] += 1.0

   for i in rig:
      if not i[0] in relrig:
         relrig[i[0]] = 0
         totrig[i[0]] = 0
      relrig[i[0]] += len(rig[i])
      totrig[i[0]] += 1.0

   s11=0
   s1n=0
   sn1=0
   snn=0
   f = open(outuputPath + "/test2id.txt", "r")
   tot = (int)(f.readline())
   for i in range(tot):
      content = f.readline()
      h,t,r = content.strip().split()
      rign = rellef[r] / totlef[r]
      lefn = relrig[r] / totrig[r]
      if (rign <= 1.5 and lefn <= 1.5):
         s11+=1
      if (rign > 1.5 and lefn <= 1.5):
         s1n+=1
      if (rign <= 1.5 and lefn > 1.5):
         sn1+=1
      if (rign > 1.5 and lefn > 1.5):
         snn+=1
   f.close()


   f = open(outuputPath + "/test2id.txt", "r")
   f11 = open(outuputPath + "/1-1.txt", "w")
   f1n = open(outuputPath + "/1-n.txt", "w")
   fn1 = open(outuputPath + "/n-1.txt", "w")
   fnn = open(outuputPath + "/n-n.txt", "w")
   fall = open(outuputPath + "/test2id_all.txt", "w")
   tot = (int)(f.readline())
   fall.write("%d\n"%(tot))
   f11.write("%d\n"%(s11))
   f1n.write("%d\n"%(s1n))
   fn1.write("%d\n"%(sn1))
   fnn.write("%d\n"%(snn))
   for i in range(tot):
      content = f.readline()
      h,t,r = content.strip().split()
      rign = rellef[r] / totlef[r]
      lefn = relrig[r] / totrig[r]
      if (rign <= 1.5 and lefn <= 1.5):
         f11.write(content)
         fall.write("0"+"\t"+content)
      if (rign > 1.5 and lefn <= 1.5):
         f1n.write(content)
         fall.write("1"+"\t"+content)
      if (rign <= 1.5 and lefn > 1.5):
         fn1.write(content)
         fall.write("2"+"\t"+content)
      if (rign > 1.5 and lefn > 1.5):
         fnn.write(content)
         fall.write("3"+"\t"+content)
   fall.close()
   f.close()
   f11.close()
   f1n.close()
   fn1.close()
   fnn.close()    
   print("...OK")
 
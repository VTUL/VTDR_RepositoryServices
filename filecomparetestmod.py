
import os
import re
from turtle import end_fill
import numpy
import numpy as np

def comparemd5txt(upack_manifestmd5,dart_manifestmd5):
  md5Upack=[]
  md5Dart=[]
  FileUpack=[]
  FileDart=[]
  f1=open(upack_manifestmd5,"r")
  for line1 in f1:
    md5line1=line1.split(' ',1)[0]
    filename1=line1.split(' ',1)[1]
    md5Upack.append(md5line1)
    FileUpack.append(filename1)

  f2=open(dart_manifestmd5,"r")
  for line2 in f2:
    md5line2=line2.split(' ',1)[0]
    filename2=line2.split(' ',1)[1]
    md5Dart.append(md5line2)
    FileDart.append(filename2)
  print("md5Upack is ",md5Upack, "\n\n"," associated file names are ",FileUpack,"\n\n\n")
  print("md5Dart is ",md5Dart, "\n\n"," associated file names are ",FileDart,"\n\n\n\n")
  xy,x,y=np.intersect1d(md5Upack,md5Dart,return_indices=True)
  Uind=[]
  Upackmd5Match=[]
  UpackFileAssMd5=[]
  for i in x:
    uindx=i.item()
    Uind.append(uindx)
    umd5=md5Upack[uindx]
    Upackmd5Match.append(umd5)
    filemd5=FileUpack[uindx]
    UpackFileAssMd5.append(filemd5)
  Dind=[]
  Dartmd5Match=[]
  DartFileAssMd5=[]
  for j in y:
    Dindx=j.item()
    Dind.append(Dindx)
    Dmd5=md5Dart[Dindx]
    Dartmd5Match.append(Dmd5)
    dfilemd5=FileDart[Dindx]
    DartFileAssMd5.append(dfilemd5)
  print("Matched md5s: ","  ","Upack ",Upackmd5Match," Dart ",Dartmd5Match, " Associated Files in UPack ",UpackFileAssMd5, " Associated files in DART ", DartFileAssMd5,"\n")

# prints the missing and additional elements in list2 
  print("Missing md5 in DART:", (set(md5Upack).difference(md5Dart)),"\n")
  missingdartmd5=set(md5Upack).difference(md5Dart)
  print("Additional md5 in DART:", (set(md5Dart).difference(md5Upack)),"\n")
  additionaldartmd5=set(md5Dart).difference(md5Upack)
  additionaldartmd5=list(additionaldartmd5)
  additionaldartfiles=[]
  for i in range(0,len(additionaldartmd5)):
    x=md5Dart.index(additionaldartmd5[i])
    additionaldartfile=FileDart[x]
    additionaldartfiles.append(additionaldartfile)
  print("Additional files in DART:", additionaldartfiles,"\n")
  print("Missing md5 in UPack:", (set(md5Dart).difference(md5Upack)),"\n")
  print("Additional md5 in UPack:", (set(md5Upack).difference(md5Dart)),"\n")
  missingupackmd5=set(md5Dart).difference(md5Upack)
  additionalupackmd5=set(md5Upack).difference(md5Dart)
  additionalupackmd5=list(additionalupackmd5)
  additionalupackfiles=[]
  for i1 in range(0,len(additionalupackmd5)):
    x1=md5Upack.index(additionalupackmd5[i1])
    additionalupackfile=FileUpack[x1]
    additionalupackfiles.append(additionalupackfile)
  print("Additional files in UPack:", additionalupackfiles)#,"\n")
 
  f2.close() 
  f1.close()  
  dictmd5=dict({'UPackmd5':md5Upack,'UPackFilenames': FileUpack,'Dartmd5': md5Dart,'DartFilenames':FileDart,'UPackmd5MatchedwithDart':Upackmd5Match,'Dartmd5MatchedwithUpack':Dartmd5Match,'UPackmd5FilesmatchedwithDart':UpackFileAssMd5,
  'Dartmd5FilesmatchedwithUpack':DartFileAssMd5,'AdditionalUpackFilesNotFoundInDart': additionalupackfiles,'AdditionalDartFilesNotFoundInUpack':additionaldartfiles,'AdditionalUpackmd5':additionalupackmd5,'AdditionalDartmd5': additionaldartmd5})    
  return dictmd5


from header import save,importRecord,check,mending
import time
import re
import os


preFileList=[]
try:
    preFileList = os.listdir("/data")
except FileNotFoundError:
    print("Folder data not found.")
    exit(-1)

fileList=[]
for fileName in preFileList:
    if(re.search(".*\.txt",fileName)!=None):
        fileList.append(fileName)
print(fileList)

for fileName in fileList:
    try:
        wordListTmp,creepingCnt,totalCreepingCntTmp,totalWordsCntTmp,uniqueWordsCntTmp,maxTimesTmp,isValidTmp=importRecord(-1,"data/"+fileName)
    except:
        mending(fileName)
    if isValidTmp is False:
        mending(fileName)
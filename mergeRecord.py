from header import save,importRecord,check
import time
import re
import os

preFileList=[]
folderName=input("Please input the folder name(/data) to merge:")
try:
    preFileList = os.listdir(folderName)
except FileNotFoundError:
    print("Folder not found.")
    exit(-1)

fileList=[]
for fileName in preFileList:
    if(re.search(".*\.txt",fileName)!=None):
        fileList.append(fileName)
print(fileList)

wordList,importCnt,totalCreepingCnt,totalWordsCnt,uniqueWordsCnt,maxTimes,isValid=importRecord(-1,"mergedData.txt")
if isValid is False:
    time.sleep(30)
    exit(-1)

for fileName in fileList:
    print("Merging file "+str(importCnt)+":\t"+fileName)
    realPath = folderName+'\\'+fileName

    wordListTmp,creepingCnt,totalCreepingCntTmp,totalWordsCntTmp,uniqueWordsCntTmp,maxTimesTmp,isValidTmp=importRecord(-1,realPath)
    if isValidTmp is False:
        time.sleep(30)
        exit(-1)

    importCnt+=1
    totalCreepingCnt+=totalCreepingCntTmp
    totalWordsCnt+=totalWordsCntTmp
    for word in wordListTmp:
        if word in wordList:
            wordList[word]+=wordListTmp[word]
        else:
            uniqueWordsCnt+=1
            wordList[word]=wordListTmp[word]

save(-1,wordList,totalWordsCnt,uniqueWordsCnt,totalCreepingCnt)
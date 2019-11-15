import time
import os


def save(NO,wordList,totalWordsCnt,uniqueWordsCnt,totalCreepingCnt):
    if NO!=-1:
        recordFileName="data/"+"record_"+str(NO)+".txt"
        processMessage="Process "+str(NO)+" :\t"
    else:
        recordFileName="mergedData.txt"
        processMessage=""

    try:
        os.stat("data")
    except:
        os.makedirs("data")

    recordFile=open(recordFileName,'w')
    maxTimes=int(sorted(wordList.values(),reverse=True)[0])
    # records=[]
    check(NO,[],wordList,totalCreepingCnt,totalWordsCnt,uniqueWordsCnt,maxTimes)
    recordFile.write("totalCreepingCnt "+str(totalCreepingCnt)+" totalWordsCnt "+str(totalWordsCnt)+" uniqueWordsCnt "+str(uniqueWordsCnt)+" maxTimes "+str(maxTimes))
    for item in sorted(wordList.items(),key=lambda x:x[1],reverse=True):
        word=item[0]
        recordFile.write("\n"+word+" "+str(item[1]))
    recordFile.close()

    if totalCreepingCnt%1000==0 and NO!=-1:
        check(NO,[],wordList,totalCreepingCnt,totalWordsCnt,uniqueWordsCnt,maxTimes)
        currentTime=str(time.strftime('%Y-%m-%d_%H-%M-%S', time.localtime(time.time())))
        backupFileName="backups/record_" +str(NO)+"/record_"+str(NO)+"_"+ currentTime + ".txt"
        try:
            os.stat("backups")
        except:
            os.makedirs("backups")
        try:
            os.stat("backups/record_"+str(NO))
        except:
            os.makedirs("backups/record_"+str(NO))
        backupFile=open(backupFileName,'w')
        recordFile = open("data/"+recordFileName, 'r')
        recordText=recordFile.read()
        backupFile.write(recordText)
        backupFile.close()
        recordFile.close()
        print(processMessage+"Backup file "+backupFileName+" created.")

    print(processMessage+"Record saved: "+"totalCreepingCnt = "+str(totalCreepingCnt)+" totalWordsCnt = "+str(totalWordsCnt)+" uniqueWordsCnt = "+str(uniqueWordsCnt))


def check(NO,records,wordList,totalCreepingCnt,totalWordsCnt,uniqueWordsCnt,maxTimes):
    if NO!=-1:
        processMessage="Process "+str(NO)+" :\t"
    else:
        processMessage=""

    realUniqueWordsCnt=int(len(wordList))
    if len(records) == 0 and uniqueWordsCnt!=0 :
        tempMax = int(sorted(wordList.values(),reverse=True)[0])
        if maxTimes != tempMax:
            print(processMessage+"Error: Record is corrupted.")
            print(processMessage+"MaxTimes should be " + str(tempMax) + " instead of " + str(maxTimes) + " .")
            return False
        else:
            print(processMessage+"Max times of the first word is examined.")
    elif len(records)>0 and maxTimes != int(records[9]):
        print(processMessage+"First time import error: Record is corrupted.")
        print(processMessage+"MaxTimes should be " + str(maxTimes) + " instead of " + str(records[9]) + " .")
        return False
    else:
        print(processMessage+"Max times of the first word is examined.")

    if realUniqueWordsCnt == uniqueWordsCnt:
        print(processMessage+"Unique words record is examined.")
    else:
        print(processMessage+"Error: Record is corrupted.")
        print(
            processMessage+"Number of unique words should be " + str(uniqueWordsCnt) + " instead of " + str(realUniqueWordsCnt) + " .")
        return False
    return True


def importRecord(NO,recordFileName):
    # import record
    processMessage=""
    if NO!=-1:
        processMessage="Process "+str(NO)+" :\t"
        try:
            os.stat("data")
        except:
            os.makedirs("data")
    try:
        os.stat(recordFileName)
    except:
        recordFile = open(recordFileName, 'w')
        recordFile.close()
    try:
        recordFile = open(recordFileName, 'r')
    except IOError:
        print(processMessage+"File not found: "+recordFileName)
        time.sleep(10)
        exit(-1)
    wordList = {}
    records = recordFile.read()
    recordFile.close()
    records = records.split()
    # print(records)
    realUniqueWordsCnt = int((len(records) - 8) / 2)
    if realUniqueWordsCnt == -4:
        realUniqueWordsCnt = 0
    print(processMessage+"Importing unique words: " + str(realUniqueWordsCnt))
    if len(records) >= 8:
        totalCreepingCnt = int(records[1])
        totalWordsCnt = int(records[3])
        uniqueWordsCnt = int(records[5])
        maxTimes = int(records[7])
    else:
        totalWordsCnt = int(0)
        uniqueWordsCnt = int(0)
        totalCreepingCnt = int(0)
        maxTimes= int(0)

    i = 8
    # print("Record:")
    wordList.clear()
    # importCnt=0
    while i <= len(records) - 2:
        if records[i] not in wordList:
            wordList[records[i]] = int(records[i + 1])
            # print(records[i] + " " + records[i + 1] , end=' , ')
            # importCnt = importCnt + 1
        else:
            print(processMessage+" Error in wordList: '"+records[i]+"'")
        i = i + 2
    # print("\nimportCnt = "+str(importCnt))

    isValid=check(NO,records,wordList,totalCreepingCnt,totalWordsCnt,uniqueWordsCnt,maxTimes)
    if isValid is True:
        print(processMessage+"File imported: totalCreepingCnt = " + str(totalCreepingCnt) + " totalWordsCnt = " + str(
            totalWordsCnt) + " uniqueWordsCnt = " + str(uniqueWordsCnt))
        records.clear()
        # finish import record
        # creepingCnt = 0
        return wordList,0,totalCreepingCnt,totalWordsCnt,uniqueWordsCnt,maxTimes,True
    else:
        return [],0,-1,-1,-1,-1,False

def mending(recordFileName):
    print("Mending "+recordFileName)
    pureFileName=os.path.splitext(recordFileName)[0]
    fullPath="/backups/"+pureFileName+"/"
    try:
        preFileList = os.listdir(fullPath)
    except FileNotFoundError:
        print("Folder "+fullPath+" not found.")
        time.sleep(30)
        exit(-1)

    fileList=[]
    for fileName in preFileList:
        if(re.search(".*\.txt",fileName)!=None):
            fileList.append(fileName)

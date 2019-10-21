import time


def save():
    global totalWordsCnt
    global uniqueWordsCnt
    global totalCreepingCnt
    global wordList
    global maxTimes
    recordFile=open("record.txt",'w')
    maxTimes=int(sorted(wordList.values(),reverse=True)[0])
    recordFile.write("totalCreepingCnt "+str(totalCreepingCnt)+" totalWordsCnt "+str(totalWordsCnt)+" uniqueWordsCnt "+str(uniqueWordsCnt)+" maxTimes "+str(maxTimes))
    for item in sorted(wordList.items(),key=lambda x:x[1],reverse=True):
        word=item[0]
        word=word.replace("'","")
        word =word.replace(",","")
        word = word.replace("[", "")
        word = word.replace("]", "")
        # print(word)
        recordFile.write("\n"+word+" "+str(item[1]))
    recordFile.close()
    time.sleep(1)
    check()
    if totalWordsCnt%1000==0:
        check()
        currentTime=str(time.strftime('%Y-%m-%d_%H-%M-%S', time.localtime(time.time())))
        backupFileName="backups/record_" + currentTime + ".txt"
        backupFile=open(backupFileName,'w')
        recordFile = open("record.txt", 'r')
        recordText=recordFile.read()
        backupFile.write(recordText)
        backupFile.close()
        recordFile.close()
        print("Backup file "+backupFileName+" created.")

    print("Record saved: "+"totalCreepingCnt = "+str(totalCreepingCnt)+" totalWordsCnt = "+str(totalWordsCnt)+" uniqueWordsCnt = "+str(uniqueWordsCnt))


def check():
    global uniqueWordsCnt
    global records
    global maxTimes
    global wordList
    global realUniqueWordsCnt
    print("\nwordList:")
    for item in sorted(wordList.items(), key = lambda kv:(kv[1], kv[0]),reverse=True):
        print(str(item[0])+" "+str(item[1]),end=" ")
    print("")
    realUniqueWordsCnt=int(len(wordList))
    if len(records) == 0 and uniqueWordsCnt!=0 :
        tempMax = int(sorted(wordList.values(),reverse=True)[0])
        if maxTimes != tempMax:
            print("Error: Record is corrupted.")
            print("MaxTimes should be " + str(tempMax) + " instead of " + str(maxTimes) + " .")
            time.sleep(60)
            exit(-1)

        print("Max times of the first word is examined.")

    if len(records)>0 and maxTimes != int(records[9]):
        print("First time import error: Record is corrupted.")
        print("MaxTimes should be " + str(maxTimes) + " instead of " + str(records[9]) + " .")
        time.sleep(60)
        exit(-1)
    else:
        print("Max times of the first word is examined.")

    if realUniqueWordsCnt == uniqueWordsCnt:
        print("Unique words record is examined.")
    else:
        print("Error: Record is corrupted.")
        print(
            "Number of unique words should be " + str(uniqueWordsCnt) + " instead of " + str(realUniqueWordsCnt) + " .")
        time.sleep(60)
        exit(-1)


# import record
recordFile = open("record.txt", 'r')
wordList = {}
records = recordFile.read()
recordFile.close()
records = records.split()
print(records)
realUniqueWordsCnt = int((len(records) - 8) / 2)
if realUniqueWordsCnt == -4:
    realUniqueWordsCnt = 0
print("Importing unique words: " + str(realUniqueWordsCnt))
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
    wordList = {}

i = 8
print("Record:")
while i <= len(records) - 2:
    wordList[records[i]] = int(records[i + 1])
    print(records[i] + " " + records[i + 1] + " ", end='')
    if wordList[records[i]]!=int(records[i + 1]) or records[i] not in wordList:
        print("Error in wordList.")
    i = i + 2

check()
print("file imported: totalCreepingCnt = " + str(totalCreepingCnt) + " totalWordsCnt = " + str(
    totalWordsCnt) + " uniqueWordsCnt = " + str(uniqueWordsCnt))
records.clear()
# finish import record

creepingCnt = 0

def save():
    global totalWordsCnt
    global uniqueWordsCnt
    global wordList
    recordFile=open("record.txt",'w')
    recordFile.write("totalWordsCnt "+str(totalWordsCnt)+" uniqueWordsCnt "+str(uniqueWordsCnt))
    for key in wordList:
        word=key
        word=word.replace("'","")
        word =word.replace(",","")
        word = word.replace("[", "")
        word = word.replace("]", "")
        # print(word)
        recordFile.write("\n"+word+" "+str(wordList[key]))
    recordFile.close()
    print("Record saved: "+"totalWordsCnt "+str(totalWordsCnt)+" uniqueWordsCnt "+str(uniqueWordsCnt))

wordList={}
totalWordsCnt = int(0)
uniqueWordsCnt =int(0)
totalCreepingCnt=int(0)
# import record
fileNumber=input("Please the number of files to merge:")
for i in range(int(fileNumber)):
    fileName=input("Please input the file name(record1.txt) to merge:")
    recordFile=open(fileName,'r')
    records=recordFile.read()
    recordFile.close()
    records=records.split()
    if len(records) >= 6:
        totalCreepingCnt = totalCreepingCnt +int(records[1])
        totalWordsCnt = totalWordsCnt+int(records[3])

    i = 6
    while i<=len(records)-2 :
        if records[i] in sorted(wordList):
            wordList[records[i]]=wordList[records[i]]+int(records[i+1])
        else:
            wordList[records[i]]=int(records[i+1])
            uniqueWordsCnt=uniqueWordsCnt+1
        i=i+2
    print("file imported: totalWordsCnt = "+str(totalWordsCnt)+" uniqueWordsCnt = "+str(uniqueWordsCnt))
# finish import record
save()
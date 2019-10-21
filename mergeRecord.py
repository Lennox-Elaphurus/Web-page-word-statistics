import header

# import header.record
fileNumber=input("Please the number of files to merge:")
for i in range(int(fileNumber)):
    fileName=input("Please input the file name(header.record1.txt) to merge:")
    try:
        header.recordFile=open(fileName,'r')
    except FileNotFoundError:
        print("File not found.")
    else:
        header.records=header.recordFile.read()
        header.recordFile.close()
    header.records=header.records.split()
    print(header.records)
    realUniqueWordsCnt = int((len(header.records) - 8) / 2)
    if realUniqueWordsCnt == -4:
        realUniqueWordsCnt = 0
    print("Importing unique words: " + str(realUniqueWordsCnt))
    if len(header.records) >= 6:
        header.totalCreepingCnt = header.totalCreepingCnt +int(header.records[1])
        header.totalWordsCnt = header.totalWordsCnt+int(header.records[3])

    if realUniqueWordsCnt == header.uniqueWordsCnt:
        print("Unique words header.records are examined.")
    else:
        print("Error: Unique words header.records is corrupted.")
        print("Number of unique words should be " + str(header.uniqueWordsCnt) + " instead of " + str(realUniqueWordsCnt) + " .")
        exit(-1)

    i = 6
    while i<=len(header.records)-2 :
        if header.records[i] in sorted(header.wordList):
            header.wordList[header.records[i]]=header.wordList[header.records[i]]+int(header.records[i+1])
        else:
            header.wordList[header.records[i]]=int(header.records[i+1])
            header.uniqueWordsCnt=header.uniqueWordsCnt+1
        i=i+2
    print("File imported: header.totalWordsCnt = "+str(header.totalWordsCnt)+" header.uniqueWordsCnt = "+str(header.uniqueWordsCnt))
# finish import header.record
header.save()
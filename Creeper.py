import re
import urllib.request
import time
import random
def save():
    global totalWordsCnt
    global uniqueWordsCnt
    global totalCreepingCnt
    global wordList
    recordFile=open("record.txt",'w')
    recordFile.write("totalCreepingCnt "+str(totalCreepingCnt)+" totalWordsCnt "+str(totalWordsCnt)+" uniqueWordsCnt "+str(uniqueWordsCnt))
    for item in sorted(wordList.items(),key=lambda x:x[1],reverse=True):
        word=item[0]
        word=word.replace("'","")
        word =word.replace(",","")
        word = word.replace("[", "")
        word = word.replace("]", "")
        # print(word)
        recordFile.write("\n "+word+" "+str(item[1]))
    recordFile.close()
    print("Record saved: "+"totalCreepingCnt "+str(totalCreepingCnt)+" totalWordsCnt "+str(totalWordsCnt)+" uniqueWordsCnt "+str(uniqueWordsCnt))

# import record
recordFile=open("record.txt",'r')
wordList={}
records=recordFile.read()
recordFile.close()
records=records.split()
print(records)
realUniqueWordsCnt=int((len(records)-6)/2)
if realUniqueWordsCnt==-3:
    realUniqueWordsCnt=0
print("Importing unique words: "+str(realUniqueWordsCnt))
if len(records)>=6:
    totalCreepingCnt = int(records[1])
    totalWordsCnt=int(records[3])
    uniqueWordsCnt = int(records[5])
else:
    totalWordsCnt = int(0)
    uniqueWordsCnt =int(0)
    totalCreepingCnt=int(0)
    wordList={}
if realUniqueWordsCnt == uniqueWordsCnt :
    print("Unique words records are examined.")
else:
    print("Error: Unique words records is corrupted.")
    print("Number of unique words should be "+str(uniqueWordsCnt)+" instead of "+str(realUniqueWordsCnt)+" .")
    exit(-1)
i=6
while i<=len(records)-2 :
    wordList[records[i]]=int(records[i+1])
    i=i+2

print("file imported: totalCreepingCnt = "+str(totalCreepingCnt)+" totalWordsCnt = "+str(totalWordsCnt)+" uniqueWordsCnt = "+str(uniqueWordsCnt))
# finish import record

creepingCnt=0
try:
    while True:
        # https://en.wikibooks.org/wiki/Special:Random
        # https://en.wikibooks.org/api/rest_v1/page/random/summary
        try:
            response = urllib.request.urlopen('https://en.wikibooks.org/api/rest_v1/page/random/html')
        except urllib.error.HTTPError:
            print("Detected an HTTP Error.")
            rest=random.randrange(30, 600)
            print("Sleeping: "+str(rest)+" s")
            time.sleep(rest)
            continue
        else:
            html = response.read()
        # getText
        formattedData=[]
        #\s \s
        # [a-zA-Z\s,.:]
        # <p>+?(?P<content>.*)</p>+?
        # r"\s(?P<content>[a-zA-Z-]+)\s"
        r"<(^[/]*)>+?(?P<content>)<(/.*)>+?"
        pattern = re.compile(r"[> '(](?P<content>[a-zA-Z-']+)[ ',.?!)<]", re.DOTALL)
        contentMatch = re.findall(pattern, str(html))
        # print(contentMatch)
        contentMatch =str(contentMatch).split()
        # finish getting words

        for content in contentMatch:
            if content in wordList.keys():
                wordList[content]=wordList[content]+1
            else:
                wordList[content]=1
                uniqueWordsCnt=uniqueWordsCnt+1
            totalWordsCnt = totalWordsCnt + 1
        # finish counting
        creepingCnt=creepingCnt+1
        if creepingCnt%10==0:
            totalCreepingCnt=totalCreepingCnt+10
            print("Creeping times: " + str(creepingCnt)+"\nSaving record...")
            save()
            print("")
        else:
            print("Creeping times: " + str(creepingCnt)+ " totalWordsCnt = " + str(
                totalWordsCnt) + " uniqueWordsCnt = " + str(uniqueWordsCnt))

        # rest=random.randrange(30, 600)
        # print("Sleeping: "+str(rest)+" s")
        # time.sleep(rest)
        # fp   = open("text.html", 'wb')
        # fp.write(html)
        # fp.close()
except KeyboardInterrupt:
    print("Detected keyboard interrupt.")
    save()
    print("Waiting, press ENTER to continue.")
save()
# fp   = open("text.html", 'wb')
# fp.write(html)
# fp.close()


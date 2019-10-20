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
    for key in wordList:
        word=key
        word=word.replace("'","")
        word =word.replace(",","")
        word = word.replace("[", "")
        word = word.replace("]", "")
        # print(word)
        recordFile.write("\n"+word+" "+str(wordList[key]))
    recordFile.close()
    print("Record saved: "+"totalCreepingCnt "+str(totalCreepingCnt)+" totalWordsCnt "+str(totalWordsCnt)+" uniqueWordsCnt "+str(uniqueWordsCnt))

# import record
recordFile=open("record.txt",'r')
wordList={}
records=recordFile.read()
recordFile.close()
records=records.split()
if len(records)>=6:
    totalCreepingCnt = int(records[1])
    totalWordsCnt=int(records[3])
    uniqueWordsCnt = int(records[5])
else:
    totalWordsCnt = int(0)
    uniqueWordsCnt =int(0)
    totalCreepingCnt=int(0)

i=6
while i<=len(records)-2 :
    wordList[records[i]]=int(records[i+1])
    i=i+2

print("file imported: totalCreepingCnt = "+str(totalCreepingCnt)+" totalWordsCnt = "+str(totalWordsCnt)+" uniqueWordsCnt = "+str(uniqueWordsCnt))
# finish import record

creepingCnt=0
while True:
    # https://en.wikibooks.org/wiki/Special:Random
    # https://en.wikibooks.org/api/rest_v1/page/random/summary
    response = urllib.request.urlopen('https://en.wikibooks.org/api/rest_v1/page/random/html')
    html = response.read()
    # getText
    formattedData=[]
    #\s \s
    # [a-zA-Z\s,.:]
    # <p>+?(?P<content>.*)</p>+?
    # r"\s(?P<content>[a-zA-Z-]+)\s"
    r"<(^[/]*)>+?(?P<content>)<(/.*)>+?"
    pattern = re.compile(r"[> '(](?P<content>[a-zA-Z-]+)[ ',.?!)<]", re.DOTALL)
    contentMatch = re.findall(pattern, str(html))
    print(contentMatch)
    contentMatch =str(contentMatch).split()
    # finish getting words

    for content in contentMatch:
        if content in wordList.keys() and content is not "totalWords":
            wordList[content]=wordList[content]+1
        else:
            wordList[content]=1
            uniqueWordsCnt=uniqueWordsCnt+1
        totalWordsCnt = totalWordsCnt + 1
    # finish counting
    creepingCnt=creepingCnt+1
    if creepingCnt%10==0:
        totalCreepingCnt=totalCreepingCnt+10
        print("Creeping times: " + str(creepingCnt))
        save()
    # rest=random.randrange(30, 600)
    # print("Sleeping: "+str(rest)+" s")
    # time.sleep(rest)
    fp   = open("text.html", 'wb')
    fp.write(html)
    fp.close()

save()
# fp   = open("text.html", 'wb')
# fp.write(html)
# fp.close()


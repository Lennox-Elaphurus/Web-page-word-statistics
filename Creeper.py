import re
import urllib.request
import time
import random
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

# import record
recordFile=open("record.txt",'r')
wordList={}
records=recordFile.read()
recordFile.close()
records=records.split()
if len(records)>=4:
    totalWordsCnt=int(records[1])
    uniqueWordsCnt = int(records[3])
else:
    totalWordsCnt = int(0)
    uniqueWordsCnt =int(0)

i=4
while i<=len(records)-2 :
    wordList[records[i]]=int(records[i+1])
    i=i+2

print("file imported: totalWordsCnt = "+str(totalWordsCnt)+" uniqueWordsCnt = "+str(uniqueWordsCnt))
# finish import record

creepingCnt=0
while(1):

    response = urllib.request.urlopen('https://en.wikibooks.org/wiki/Special:Random')
    html = response.read()
    # getText
    formattedData=[]
    #\s \s
    # [a-zA-Z\s,.:]
    # <p>+?(?P<content>.*)</p>+?
    pattern = re.compile(r"\s(?P<content>[a-zA-Z]+)\s", re.DOTALL)
    contentMatch = re.findall(pattern, str(html))
    # print(contentMatch)
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
    # if creepingCnt%10==0:
    print("Creeping times: " + str(creepingCnt))
    save()
    rest=random.randrange(30, 600)
    print("Sleeping: "+str(rest)+" s")
    time.sleep(rest)

save()
# fp   = open("text.html", 'wb')
# fp.write(html)
# fp.close()


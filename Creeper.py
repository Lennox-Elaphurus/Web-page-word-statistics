import re
import urllib.request
import urllib.error
import time
import random
import header

try:
    while True:
        # https://en.wikibooks.org/wiki/Special:Random
        # https://en.wikibooks.org/api/rest_v1/page/random/summary
        try:
            response = urllib.request.urlopen('https://en.wikibooks.org/api/rest_v1/page/random/html')
        except urllib.error.HTTPError:
            print("Detected an HTTP Error.")
            rest=random.randrange(30, 60)
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
            if content in header.wordList.keys():
                header.wordList[content]=header.wordList[content]+1
            else:
                header.wordList[content]=int(1)
                header.uniqueWordsCnt=header.uniqueWordsCnt+1
            header.totalWordsCnt = header.totalWordsCnt + 1
        # finish counting
        header.creepingCnt=header.creepingCnt+1
        print(str(time.strftime('%H:%M:%S', time.localtime(time.time())))+" Creeping times " + str(header.creepingCnt) + " :\tgot " + str(len(contentMatch)) + " words.")
        if header.creepingCnt%10==0:
            header.totalCreepingCnt=header.totalCreepingCnt+10
            print("Saving record, please don't exit.")
            header.save()
            print("")
            time.sleep(1)

        # fp   = open("text.html", 'wb')
        # fp.write(html)
        # fp.close()
except KeyboardInterrupt:
    print("Detected keyboard interrupt.")
    print("Waiting, press ENTER to exit.")
    time.sleep(60)
    exit(0)
else:
    print("Detected an unexpected error.")
    time.sleep(60)
    exit(-1)
# fp   = open("text.html", 'wb')
# fp.write(html)
# fp.close()


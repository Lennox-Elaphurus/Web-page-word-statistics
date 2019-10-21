import re
import requests
import time
import random
import header

try:
    while True:
        # https://en.wikibooks.org/wiki/Special:Random
        # https://en.wikibooks.org/api/rest_v1/page/random/summary
        try:
            response = requests.get('https://en.wikibooks.org/api/rest_v1/page/random/html').text
        except requests.HTTPError:
            print("Detected an HTTP Error.")
            rest=random.randrange(30, 60)
            print("Sleeping: "+str(rest)+" s")
            time.sleep(rest)
            continue
        else:
            html = response
            # print(html)
        # getText
        formattedData=[]
        #\s \s
        # [a-zA-Z\s,.:]
        # <p>+?(?P<content>.*)</p>+?
        # r"\s(?P<content>[a-zA-Z-]+)\s"
        # r"<(^[/]*)>+?(?P<content>)<(/.*)>+?"
        # (? <= <[a-zA-Z]+ >). * (?= < /[a-zA-Z]+ >)
        pattern0=re.compile(">+?(?P<content>[^<>=|&]+)<+?", re.DOTALL)
        html=str(html).replace("\n"," ")
        html = html.replace("\t", " ")
        html = html.replace("/", " ")
        html = html.replace("\"", " ")
        preMatches=re.findall(pattern0, str(html))
        # print(preMatches)
        # r"[> '(]+(?P<content>[a-zA-Z-']+)[ ',.?!)<]+"
        pattern1 = re.compile(r"[ ]+(?P<content>[a-zA-Z-']+)[ ,.?!:]+", re.DOTALL)
        contentMatch=[]
        for preMatch in preMatches:
            contentMatch.extend(re.findall(pattern1, str(" "+preMatch+" ")))
            # print(re.findall(pattern1, " "+str(preMatch)+" "),end=" ")
        # print("")
        # print(contentMatch)
        # finish getting words

        for content in contentMatch:
            content=content.strip("'")
            content = content.strip("-")
            if content in header.wordList.keys():
                header.wordList[content]=header.wordList[content]+1
            elif len(content)>0 and content[0]!="-" and content[len(content)-1]!="-":
                try:
                    print(header.wordList[content])
                    print("Error in wordList.")
                    print(str(header.wordList[content]) + " already exist.")
                except :
                    header.wordList[content]=int(1)
                header.uniqueWordsCnt=header.uniqueWordsCnt+1
            header.totalWordsCnt = header.totalWordsCnt + 1
        # finish counting
        header.creepingCnt=header.creepingCnt+1
        print(str(time.strftime('%H:%M:%S', time.localtime(time.time())))+" Creeping times " + str(header.creepingCnt) + " : got " + str(len(contentMatch)) + " words.")
        if header.creepingCnt%10==0:
            header.totalCreepingCnt=header.totalCreepingCnt+10
            print("Saving record, please don't exit.")
            header.save()
            print("")

        # fp   = open("text.html", 'w',encoding="utf-8")
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


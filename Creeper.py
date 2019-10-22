import re
import requests
import time
import random
import os
from header import save,importRecord
from multiprocessing import Pool


def crawling(NO):
    print('Child process %s.' % os.getpid())
    recordFileName="record_"+str(NO)+".txt"
    wordList,realUniqueWordsCnt,creepingCnt,totalCreepingCnt,totalWordsCnt,uniqueWordsCnt,maxTimes=importRecord(recordFileName)
    terminate=False
    try:
        while terminate is False:
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
                if content in wordList.keys():
                    wordList[content]=wordList[content]+1
                elif len(content)>0 and content[0]!="-" and content[len(content)-1]!="-":
                    try:
                        print(wordList[content])
                        print("Error in wordList.")
                        print(str(wordList[content]) + " already exist.")
                    except :
                        wordList[content]=int(1)
                    uniqueWordsCnt=uniqueWordsCnt+1
                totalWordsCnt = totalWordsCnt + 1
            # finish counting
            creepingCnt=creepingCnt+1
            print(str(time.strftime('%H:%M:%S', time.localtime(time.time())))+" Creeping times " + str(creepingCnt) + " : got " + str(len(contentMatch)) + " words.")
            if creepingCnt%10==0:
                totalCreepingCnt=totalCreepingCnt+10
                print("Saving record, please don't exit.")
                save(NO,wordList,totalWordsCnt,uniqueWordsCnt,totalCreepingCnt)
                print("")
                terminate=True

            # fp   = open("text.html", 'w',encoding="utf-8")
            # fp.write(html)
            # fp.close()
    except KeyboardInterrupt:
        print("Detected keyboard interrupt in process "+str(NO)+" .")
        print("Waiting, press ENTER to exit.")
        time.sleep(10)
        exit(0)
    else:
        print("Detected an unexpected error.")
        time.sleep(10)
        exit(-1)
    # fp   = open("text.html", 'wb')
    # fp.write(html)
    # fp.close()


#_________________________main________________________________

if __name__=='__main__':
    print('Parent process %s.' % os.getpid())
    p = Pool(4)
    for i in range(4):
        p.apply_async(crawling(i))
    print('Waiting for all subprocesses done...')
    p.close()
    p.join()
    print('All subprocesses done.')
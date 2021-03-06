import re
import requests
import time
import random
import os
from header import save,importRecord,maintain,getConfig,writeConfig
from multiprocessing import Pool
import multiprocessing


def crawling(NO):
    processMessage="Process "+str(NO)+" :\t"
    print('Child process '+str(NO)+" started.")
    recordFilePath="data/record_"+str(NO)+".txt"

    wordList,creepingCnt,totalCreepingCnt,totalWordsCnt,uniqueWordsCnt,maxTimes,isValid=importRecord(NO,recordFilePath)
    if isValid is False:
        time.sleep(30)
        exit(-1)

    terminate="False"
    try:
        while terminate == "False":
            # https://en.wikibooks.org/wiki/Special:Random
            # https://en.wikibooks.org/api/rest_v1/page/random/summary
            try:
                response = requests.get('https://en.wikibooks.org/api/rest_v1/page/random/html').text
            except requests.HTTPError:
                print(processMessage+"Detected an HTTP Error.")
                rest=random.randrange(30, 60)
                print(processMessage+"Sleeping: "+str(rest)+" s")
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
            pattern0=re.compile(">+?(?P<content>[^<>=|\\\{\}\[\]&]+)<+?", re.DOTALL)
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
                        print(processMessage+"Error in wordList.")
                        print(processMessage+str(wordList[content]) + " already exist.")
                    except :
                        wordList[content]=int(1)
                    uniqueWordsCnt=uniqueWordsCnt+1
                totalWordsCnt = totalWordsCnt + 1
            # finish counting
            creepingCnt=creepingCnt+1
            print(processMessage+str(time.strftime('%H:%M:%S', time.localtime(time.time())))+" Creeping times " + str(creepingCnt) + " : got " + str(len(contentMatch)) + " words.")
            if creepingCnt%50==0:
                totalCreepingCnt=totalCreepingCnt+50
                print(processMessage+"Saving record, please don't exit.")
                save(NO,wordList,totalWordsCnt,uniqueWordsCnt,totalCreepingCnt)
                print("")
                processCnt,terminate=getConfig()

            # fp   = open("text.html", 'w',encoding="utf-8")
            # fp.write(html)
            # fp.close()
    except KeyboardInterrupt:
        print(processMessage+"Detected keyboard interrupt in process "+str(NO)+" .")
        print(processMessage+"Waiting, press ENTER to exit.")
        time.sleep(10)
        exit(0)
    else:
        print('Child process '+str(NO)+ " closed.")
    # fp   = open("text.html", 'wb')
    # fp.write(html)
    # fp.close()

#_________________________main________________________________
if __name__=='__main__':
    # very necessary when your are in windows
    multiprocessing.freeze_support()

    print('Parent process %s.' % os.getpid())
    processCnt,terminate=getConfig()
    # maintain()

    pool = Pool(processes=processCnt)
    for i in range(processCnt):
        pool.apply_async(crawling,args=(i,))

    print('Waiting for all subprocesses done...')
    pool.close()
    pool.join()
    print('All subprocesses done.')

    processCnt,terminate=getConfig()
    terminate="False"
    writeConfig(processCnt,terminate)
    print("You can exit the program now.")
    time.sleep(5)
else:
    print("In child process.")
    time.sleep(10)
    exit(-1)

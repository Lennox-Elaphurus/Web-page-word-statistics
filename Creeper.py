import re
import requests
import time
import random
import os
from header import save,importRecord
from multiprocessing import Pool
import multiprocessing
from bs4 import BeautifulSoup


def crawling(NO):
    processMessage="Process "+str(NO)+" :\t"
    print('Child process '+str(NO)+" started.")
    recordFilePath="data/record_"+str(NO)+".txt"
    wordList,creepingCnt,totalCreepingCnt,totalWordsCnt,uniqueWordsCnt,maxTimes=importRecord(NO,recordFilePath)
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
            # else:
            #     html = response
                # print(html)
            # # getText
            # #\s \s
            # # [a-zA-Z\s,.:]
            # # <p>+?(?P<content>.*)</p>+?
            # # r"\s(?P<content>[a-zA-Z-]+)\s"
            # # r"<(^[/]*)>+?(?P<content>)<(/.*)>+?"
            # # (? <= <[a-zA-Z]+ >). * (?= < /[a-zA-Z]+ >)
            # pattern0=re.compile(">+?(?P<content>[^<>=|&]+)<+?", re.DOTALL)
            # html=str(html).replace("\n"," ")
            # html = html.replace("\t", " ")
            # html = html.replace("/", " ")
            # html = html.replace("\"", " ")
            # preMatches=re.findall(pattern0, str(html))
            # # print(preMatches)
            # # r"[> '(]+(?P<content>[a-zA-Z-']+)[ ',.?!)<]+"
            # pattern1 = re.compile(r"[ ]+(?P<content>[a-zA-Z-']+)[ ,.?!:]+", re.DOTALL)
            # contentMatch=[]
            # for preMatch in preMatches:
            #     contentMatch.extend(re.findall(pattern1, str(" "+preMatch+" ")))
            #     # print(re.findall(pattern1, " "+str(preMatch)+" "),end=" ")
            # # print("")
            # # print(contentMatch)
            # # finish getting words
            my_soup = BeautifulSoup(response, 'html.parser')
            contentMatch=my_soup.get_text()
            symbols = "!@#$%^&*()_+={[}]|\;:\"?/.,"
            for i in range(0, len(symbols)):
                contentMatch = contentMatch.replace(symbols[i], ' ')
            contentMatch=contentMatch.split()
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
            if creepingCnt%10==0:
                totalCreepingCnt=totalCreepingCnt+10
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


def getConfig():
    try:
        os.stat("config.txt")
    except:
        configFile = open("config.txt", 'w')
        configFile.write("processes= "+str(10)+" terminate= False")
        configFile.close()

    configFile = open("config.txt", 'r')
    configs=configFile.read()
    configs=configs.split()
    processCnt=int(configs[1])
    if processCnt>200:
        processCnt=200
        print("The maximum number of processes is 200.")
    terminate=configs[3]
    return processCnt,terminate


def writeConfig(processCnt,terminate):
    configFile = open("config.txt", 'w')
    configFile.write("processes= "+str(processCnt)+" terminate= "+terminate)
    configFile.close()


#_________________________main________________________________
# if __name__=='__main__':
#     # 当在Windows上打包时，multiprocessing.freeze_support()这行非常必要
#     # 在Linux和Mac上打包用不着
#     multiprocessing.freeze_support() #只要在你的程序的入口中加上这行代码加上就可以了
#
#     print('Parent process %s.' % os.getpid())
#     processCnt,terminate=getConfig()
#
#     pool = Pool(processes=processCnt)
#     for i in range(processCnt):
#         pool.apply_async(crawling,args=(i,))
#
#     print('Waiting for all subprocesses done...')
#     pool.close()
#     pool.join()
#     print('All subprocesses done.')
#
#     processCnt,terminate=getConfig()
#     terminate="False"
#     writeConfig(processCnt,terminate)
#     print("You can exit the program now.")
#     time.sleep(5)
# else:
#     print("In child process.")
#     time.sleep(10)
#     exit(-1)
crawling(0)
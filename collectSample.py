import requests
import time
import random
import os
from header import getConfig
from bs4 import BeautifulSoup
from multiprocessing import Pool
import multiprocessing

def crawlingSample(NO):
    processMessage="Process "+str(NO)+" :\t"
    print('Child process '+str(NO)+" started.")
    terminate="False"
    cntA=0
    try:
        os.stat("sample")
    except:
        os.makedirs("sample")
    try:
        text=""
        while terminate == "False":
            cntA+=1
            print(processMessage+"Creeping "+cntA)
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
                soup = BeautifulSoup(response, 'html.parser')
                text=soup.get_text()+text

            if cntA%100==0:
                currentTime = str(time.strftime('%Y-%m-%d_%H-%M-%S', time.localtime(time.time())))
                fp   = open("sample/"+currentTime+".txt", 'w',encoding="utf-8")
                fp.write(text)
                fp.close()
                text=""
                print(currentTime+".txt Saved.")
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


# _________________________main________________________________
if __name__=='__main__':
    # very necessary when your are in windows
    multiprocessing.freeze_support()

    print('Parent process %s.' % os.getpid())
    processCnt,terminate=getConfig()
    # maintain()

    pool = Pool(processes=processCnt)
    for i in range(processCnt):
        pool.apply_async(crawlingSample,args=(i,))

    print('Waiting for all subprocesses done...')
    pool.close()
    pool.join()
    print('All subprocesses done.')
    time.sleep(5)
else:
    print("In child process.")
    time.sleep(10)
    exit(-1)

# crawlingSample(-1)

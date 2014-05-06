__author__ = 'sony'
import urllib.request
import re
import sys
import os
import inspect
import getopt
import queue
import threading
from bs4 import BeautifulSoup

class MyThread(threading.Thread):
    def __init__(self, myQueue, picPath):  # passing myQueue
        print("init")
        threading.Thread.__init__(self)
        self.myQueue = myQueue
        self.picPath = picPath

    def run(self):
        print("download")
        while self.myQueue.empty() is False:
            imgUrl = self.myQueue.get()
            num = imgUrl.rfind('/')
            imgName = imgUrl[(num+1):]
            #urllib.request.urlretrieve(imgUrl,"F:\img\\"+imgname,reporthook)
            try:
                urllib.request.urlretrieve(imgUrl, self.picPath+imgName)
            except Exception as err:
                print(imgName, err)
                #save the imgUrl that haven't been downloaded
                self.myQueue.put(imgUrl)
            if self.myQueue.empty():
                print("finished")
                break


class MyUrlThread(threading.Thread):
    def __init__(self, myUrlQueue, mySeenQueue, myPicGroupQueue, picNum):  # passing myQueue
        print("init")
        threading.Thread.__init__(self)
        self.myUrlQueue = myUrlQueue
        self.mySeenQueue = mySeenQueue
        self.myPicGroupQueue = myPicGroupQueue
        self.picNum = picNum
        #self.initUrl = "http://www.22mm.cc/"
    def run(self):
        print("crawler")
        #contentUrlList = []
        #columnUrlList = []
        #indexUrlList = []
        while True:
            if self.myUrlQueue.empty() is False:
                url = self.myUrlQueue.get()
                innerUrlHtml = getHtml(url)
                soup = BeautifulSoup(innerUrlHtml)
                urlList = soup.findAll('a', href=re.compile(r'/mm/\S+'))
                rawIndexUrl = soup.findAll('a', href=re.compile(r'index\S+html'))
                curUrl = soup.find(attrs={"class": "cur"})
                print(curUrl)
                print("cur", curUrl['href'])
                if len(rawIndexUrl) != 0:  # http://www.22mm.cc/mm/qingliang/index.html
                    print(rawIndexUrl)
                    for i in range(0, len(rawIndexUrl)):
                        indexUrl = "http://www.22mm.cc"+curUrl['href']+rawIndexUrl[i]['href']
                        seen = self.mySeenQueue.get()
                        if indexUrl not in seen:
                            seen.add(indexUrl)
                            self.mySeenQueue.put(seen)
                            self.myUrlQueue.put(indexUrl)
                        else:
                            self.mySeenQueue.put(seen)
                print("~~~~~~~~~~~~")
                for i in range(0, len(urlList)):
                    innerUrl = urlList[i]['href']
                    innerUrl = "http://www.22mm.cc"+innerUrl
                    if innerUrl.endswith(".html") is True and innerUrl.endswith("/rec.html") is False:  # http://www.22mm.cc/mm/qingliang/PiaidemeJJPaimmHm.html
                        seen = self.mySeenQueue.get()
                        if innerUrl not in seen:
                            seen.add(innerUrl)
                            self.mySeenQueue.put(seen)
                            innerHtml = getHtml(innerUrl)
                            pattern = re.compile(r'</span>/\d+</strong>')
                            innerHtmlNumSpan = pattern.findall(innerHtml)[0]
                            innerHtmlNumSpan = innerHtmlNumSpan.replace('</span>/', '')
                            innerHtmlNumStr = innerHtmlNumSpan.replace('</strong>', '')
                            innerHtmlNum = int(innerHtmlNumStr)
                            picHtml = innerUrl[0:-5]+"-"+str(innerHtmlNum)+".html"
                            if self.picNum != -1 and self.myPicGroupQueue.qsize() <= self.picNum/10:
                                self.myPicGroupQueue.put(picHtml)
                            elif self.picNum == -1:
                                self.myPicGroupQueue.put(picHtml)
                            else:
                                break
                        else:
                            self.mySeenQueue.put(seen)
                        #contentUrlList.append(innerUrl)
                    else:  # http://www.22mm.cc/mm/jingyan/
                        seen = self.mySeenQueue.get()
                        if innerUrl not in seen:
                            seen.add(innerUrl)
                            self.mySeenQueue.put(seen)
                            self.myUrlQueue.put(innerUrl)
                        else:
                            self.mySeenQueue.put(seen)
                #print(contentUrlList)
                #print(columnUrlList)
                print("=============")
                print("", self.myUrlQueue.qsize())
                print("", self.mySeenQueue.qsize())
                print("size", self.myPicGroupQueue.qsize())
            else:
                break
        #return
        callback()


'''
def reporthook(a, b, c):
    #print(a,b,c)
    percent = a*b/c*100
    if percent > 100:
        percent = 100
    print("%d %d"%(percent, (count+(a*b/c))/len(myItems)*100))
'''
def callback():
    print("done")

def getHtml(url):
    try:
        fp = urllib.request.urlopen(url)
    except Exception as err:
        print("err", err)
        fp = urllib.request.urlopen(url)
    mybytes = fp.read()
    # note that Python3 does not read the html code as string
    # but as html code bytearray, convert to string with
    html = mybytes.decode("utf8")
    fp.close()
    if html is not None:
        return html



def getHtmlList():
    htmlList = []
    url = "http://www.22mm.cc/"
    html = getHtml(url)
    pattern = re.compile(r'/mm/[a-z]+/[A-Z][A-Za-z]+.html')
    rawHtmlList = pattern.findall(html)
    for count in range(0, len(rawHtmlList)):
        rawHtmlList[count] = "http://www.22mm.cc"+rawHtmlList[count]
        innerHtml = getHtml(rawHtmlList[count])
        pattern = re.compile(r'</span>/\d+</strong>')
        innerHtmlNumSpan = pattern.findall(innerHtml)[0]
        innerHtmlNumSpan = innerHtmlNumSpan.replace('</span>/', '')
        innerHtmlNumStr = innerHtmlNumSpan.replace('</strong>', '')
        innerHtmlNum = int(innerHtmlNumStr)
        picHtml = rawHtmlList[count][0:-5]+"-"+str(innerHtmlNum)+".html"
        htmlList.append(picHtml)
    return htmlList


def getImgList(htmlList):
    imgList = []
    for i in range(0, len(htmlList)):
        html = getHtml(htmlList[i])
        pattern = re.compile(r'0]="http://\S*?.jpg')
        rawImgList = pattern.findall(html)
        for n in range(0, len(rawImgList)):
            rawImgList[n] = rawImgList[n].replace('0]="', '')
            rawImgList[n] = rawImgList[n].replace('big', 'pic')
            imgList.append(rawImgList[n])
    return imgList


def getUrl(myUrlQueue, mySeenQueue, myPicGroupQueue, argvList):
    for i in range(0, argvList[0]):
        myUrlThread = MyUrlThread(myUrlQueue, mySeenQueue, myPicGroupQueue,argvList[2])
        myUrlThread.start()


def download(myQueue, argvList):
    for i in range(0, argvList[0]):  # number of thread
        myThread = MyThread(myQueue, argvList[1])
        myThread.start()


def myHelp():
    print("-h 程序运行帮助")
    print("-n 设定线程数量(默认为10)")
    print("-o 设定图片存储目录（如d:\pics 默认为当前目录下的pics目录）")
    print("-l 设定爬取图片数量（默认不限制）")


def initOpt(argvList):
    print("before", argvList)
    opts, args = getopt.getopt(sys.argv[1:], "hn:o:l:")
    for op, value in opts:
        if op == "-h":
            myHelp()
            sys.exit()
        elif op == "-n" and int(value) > 0:
            argvList[0] = int(value)
        elif op == "-o":
            argvList[1] = value+"\\"
        elif op == "-l" and int(value) > 0:
            argvList[2] = int(value)


def main():
    caller_file = inspect.stack()[1][1]
    path = os.path.abspath(os.path.dirname(caller_file))
    print(path)
    argvList = [10, path+"\\pics\\", -1]  # threadNum,savePath,picNum
    initOpt(argvList)
    if os.path.exists(argvList[1]) is False:  # make dir
        os.mkdir(argvList[1])
    #htmlList = getHtmlList()  # get htmlList
    initUrl = "http://www.22mm.cc/"
    myUrlQueue = queue.Queue()
    mySeenQueue = queue.Queue()
    myPicGroupQueue = queue.Queue()
    seen = set()
    seen.add(initUrl)
    myUrlQueue.put(initUrl)
    mySeenQueue.put(seen)
    print("siz",mySeenQueue.qsize())
    #htmlList = getUrl(myUrlQueue, mySeenQueue, myPicGroupQueue, argvList)
    getUrl(myUrlQueue, mySeenQueue, myPicGroupQueue, argvList)
    '''
    无法等线程结束后才对htmlList赋值
    '''
    htmlList = []
    for i in range(0, myPicGroupQueue.qsize()):
        htmlList = myPicGroupQueue.get()
    print(htmlList)

    imgList = getImgList(htmlList)  # get pic URL
    print(imgList)
    myQueue = queue.Queue()  # init queue
    if argvList[2] != -1 and argvList[2] <= len(imgList):
        for i in range(0, argvList[2]):
            myQueue.put(imgList[i])
    else:
        for i in range(0, len(imgList)):
            myQueue.put(imgList[i])
    download(myQueue, argvList)

main()

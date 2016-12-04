import random
import threading
import urllib.request
import re
from urllib.error import HTTPError
from PIL import Image
import os
import http.client

http.client.HTTPConnection._http_vsn = 10
http.client.HTTPConnection._http_vsn_str = 'HTTP/1.0'
url = "http://konachan.com/post/show/"
check=1
filesize = 0
imgpath="img"#图片存放路径
maxuse=4000#最大单次爬取文件大小
limitsize_x=1300
limitsize_y=768#最小图片大小限制
list=[]
exitFlag = 0
threadnum=2#线程数量
startnum=0#开始id
endnum=10#结束id
if not os.path.exists(r"img"):
        os.mkdir("img")
if os.path.exists("list"):
    file = open("list","r")
    for line in file:
        list.append(int(line.replace('\n','')))
    file.close()
else:
    for i in range(startnum,endnum):
        list.append(i)
        file = open("list", "a+")
        file.write(str(i) + "\n")

def imgCheck(fileName):
        image = Image.open(fileName)
        imgSize = image.size
        maxsize = max(imgSize)
        minsize = min(imgSize)
        if maxsize<limitsize_x :
                if minsize<limitsize_y:
                        image.close()
                        os.remove(fileName)
                        return 0

def getImg(html):
    global filesize
    reg = r'highres-show" href="(.+?)"'
    imgre = re.compile(reg)
    imglist = re.findall(imgre, html)
    if len(imglist) == 0:
        return "empty"
    splited = imglist[0].split("/")
    fileName = splited[len(splited) - 1]
    if fileName.find("nipples") > 0:
        return "nipples"
    if fileName.find("pussy") > 0:
        return "pussy"
    if fileName.find("sex") > 0:
        return "sex"
    if fileName.find("penis") > 0:
        return "penis"
    if fileName.find("kiss") > 0:
        return "kiss"
    if fileName.find("spread_legs") > 0:
        return "spread_legs"
    if fileName.find("vibrator") > 0:
        return "vibrator"
    if fileName.find("fujima_takuya") > 0:
        return "fujima_takuya"
    if fileName.find("no_bar") > 0:
        return "nobar"
    if fileName.find("breast_hold") > 0:
        return "breast_hold"
    if fileName.find("cum") > 0:
        return "cum"
    if fileName.find("nude") > 0:
        return "nude"
    if fileName.find("bondage") > 0:
        return "bondage"
    if fileName.find("cunnilingus") > 0:
        return "cunnilingus"
    fileName = imgpath + "/" + fileName
    try:
        urllib.request.urlretrieve(imglist[0], fileName)
    except:
        return "error"
    filesize += os.path.getsize(fileName) / 1024.0 / 1024.0
    if filesize > maxuse:
        print("out of max size")
        exit(0)

    if imgCheck(fileName) == 0:
        return "too small"
    return fileName

def getHtml(url):
    try:
        page = urllib.request.urlopen(url)
        html = page.read()
        html = html.decode('UTF-8')
    except HTTPError as e:
        global check
        check = 0
        return e.reason
    return html

class imgThread(threading.Thread):
    def __init__(self, threadID, name):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name

    def run(self):
        print("开始线程：" + self.name)
        get(self.name)
        print("退出线程：" + self.name)

def get(threadName):
    global exitFlag
    while len(list) != 0:
        if exitFlag:
            threadName.exit()
        lenn = len(list)
        num = random.randint(0, lenn - 1)
        trueurl = url + str(list[num])
        tmp = str(list[num])
        html = getHtml(trueurl)
        request = getImg(html)
        print(threadName+":"+str(tmp)+":"+request)
        threadLock.acquire()
        file = open("list", "w+")
        try:
            if request!="error":
                list.remove(list[num-1])
        except:
            continue
        for i in range(0,len(list)-1):
            file.write(str(list[i]) + "\n")
        output = open('out', 'a')
        output.write(threadName+":"+str(tmp) + ":" + getImg(html) + "\n")
        output.flush()
        output.close()
        file.close()
        threadLock.release()

    exitFlag = 1
threadLock = threading.Lock()
threads=[]
for i in range(1,threadnum+1):
    tmp=imgThread(i, "Thread-"+str(i))
    tmp.start()
    threads.append(tmp)
for t in threads:
    t.join()

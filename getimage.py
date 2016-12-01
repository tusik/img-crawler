import urllib.request
import time
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
if not os.path.exists(imgpath):
        os.mkdir(imgpath)
def getHtml(url):
        try:
                page = urllib.request.urlopen(url)
                html = page.read()
                html = html.decode('UTF-8')
        except:
                global check
                check = 0
                return "error"
        return html

def imgCheck(fileName):
        image = Image.open(fileName)
        imgSize = image.size
        maxsize = max(imgSize)
        minsize = min(imgSize)
        if maxsize<1300 :
                if minsize<768:
                        image.close()
                        os.remove(fileName)
                        return 0

def getImg(html):
        global filesize
        reg = r'highres-show" href="(.+?)"'
        imgre = re.compile(reg)
        imglist = re.findall(imgre,html)
        if len(imglist)==0:
                return "empty"
        splited = imglist[0].split("/")
        fileName = splited[len(splited)-1]
        if fileName.find("nipples")>0:
                return "nipples"
        if fileName.find("pussy")>0:
                return "pussy"
        if fileName.find("sex")>0:
                return "sex"
        if fileName.find("penis")>0:
                return "penis"
        if fileName.find("kiss")>0:
                return "kiss"
        if fileName.find("spread_legs")>0:
                return "spread_legs"
        if fileName.find("vibrator")>0:
                return "vibrator"
        if fileName.find("fujima_takuya")>0:
                return "fujima_takuya"
        if fileName.find("no_bar")>0:
                return "nobar"
        if fileName.find("breast_hold")>0:
                return "breast_hold"
        if fileName.find("cum")>0:
                return "cum"
        if fileName.find("nude")>0:
                return "nude"
        if fileName.find("bondage")>0:
                return "bondage"
        if fileName.find("cunnilingus")>0:
                return "cunnilingus"
        fileName = imgpath+"/"+fileName
        urllib.request.urlretrieve(imglist[0],fileName )
        filesize+=os.path.getsize(fileName)/1024.0/1024.0
        if filesize > maxuse:
                print("out of max size")
                exit(0)

        if imgCheck(fileName)==0:
                return "too small"
        return fileName

for i in range(1,300000):#爬取范围
        trueurl = url+str(i)
        html = getHtml(trueurl)
        if html=="error":
                continue
        if i%3==0:
                time.sleep(1)
        output = open('out', 'a')
        outcount = open('count', 'w+')
        outcount.write(str(i))
        output.write(str(i)+": "+getImg(html)+"\n")
        output.flush()
        output.close()
        outcount.flush()
        outcount.close()
import json,os,re
import urllib.request
url=r'http://konachan.com/post.json?page='
proxy_handler = urllib.request.ProxyHandler({'http': 'http://127.0.0.1:1087/'})
opener = urllib.request.build_opener(proxy_handler)
urllib.request.install_opener(opener)
ext_path="ext"
path="img"
tags=[]
ids=[]
created_ats=[]
creator_ids=[]
authors=[]
changes=[]
sources=[]
scores=[]
file_sizes=[]
file_urls=[]
widths=[]
heights=[]
keyWords=['nipples','penis','sex','kiss','spread_legs','pussy','cum','cunnilingus']
if not os.path.exists(path):
        os.mkdir(path)
if not os.path.exists(ext_path):
        os.mkdir(ext_path)
        for i in keyWords:
            os.mkdir(ext_path+"/"+i)
import re
 
def validateTitle(title):
    rstr = r"[\/\\\:\*\?\"\<\>\|]" 
    new_title = re.sub(rstr, "_", title) 
    return new_title
def getHtml(url):
    try:
        html = opener.open(url)
    except:
        global check
        check = 0
        return "ERROR : CAN NOT GET CONTENT"
    return html.read()
def getInfo(html):
    jsons=json.loads(html)
    return jsons
def splitInfo(obj):
    for tmp in obj:
        tags.append(tmp['tags'])
        ids.append(tmp['id'])
        # created_ats.append(tmp['created_at'])
        # creator_ids.append(tmp['creator_id'])
        # authors.append(tmp['author'])
        # changes.append(tmp['change'])
        # sources.append(tmp['source'])
        widths.append(tmp['width'])
        heights.append(tmp['height'])
        scores.append(tmp['score'])
        file_sizes.append(tmp['file_size'])
        file_urls.append(tmp['file_url'])
def download():
    output = open('out', 'a')
    for i in range(0,len(file_urls)):
        try:
            sex_flag = False
            ext = ''
            tmps = file_urls[i].split(".")
            # print(tmps[len(tmps)-1])
            for t in keyWords:
                if tags[i].find(t)!=-1:
                    output.write(str(ids[i]) + ": " + t + "\n")
                    print(str(ids[i]) + ": " + t + "\n")
                    sex_flag=True
                    ext = t
                    break

            output.write(str(ids[i]) + ": " + tags[i] + "." + tmps[len(tmps) - 1] + "\n")
            print(str(ids[i]) + ": " + tags[i] + "." + tmps[len(tmps) - 1] + "\n")

            if len(tags[i]) > 140:
                fileName = (ext_path+'/'+ext if sex_flag else path) + "/" + str(ids[i]) + "_" + validateTitle(tags[i][0:130]) + "." + tmps[len(tmps) - 1]
            else:
                fileName = (ext_path+'/'+ext if sex_flag else path)+"/"+str(ids[i]) + "_" + validateTitle(tags[i])+"."+tmps[len(tmps)-1]
            if file_urls[i].find('http')>=0:
                download_url = file_urls[i]
            else: 
                download_url = "http:"+file_urls[i]
            print(fileName)
            urllib.request.urlretrieve(download_url,fileName)
        except Exception as e:
            print(e)
            output.write(str(ids[i]) + ": " + "failed" + "\n")
            return "failed"
        output.flush()

    output.close()

if __name__=='__main__':
    for i in range(1,2):
        splitInfo(getInfo(getHtml(url+str(i))))
        download()
        tags.clear()
        ids.clear()
        scores.clear()
        file_urls.clear()
        file_sizes.clear()
        print("page "+str(i)+" done")
    print(file_urls)
import json,os
import urllib.request
url=r'http://konachan.com/post.json?page='
proxy_handler = urllib.request.ProxyHandler({'http': 'http://127.0.0.1:1080/'})
opener = urllib.request.build_opener(proxy_handler)
urllib.request.install_opener(opener)
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

            tmps = file_urls[i].split(".")
            # print(tmps[len(tmps)-1])
            for t in keyWords:
                if tags[i].find(t)!=-1:
                    output.write(str(ids[i]) + ": " + t + "\n")
                    print(str(ids[i]) + ": " + t + "\n")
                    continue

            output.write(str(ids[i]) + ": " + tags[i] + "." + tmps[len(tmps) - 1] + "\n")
            print(str(ids[i]) + ": " + tags[i] + "." + tmps[len(tmps) - 1] + "\n")

            if len(tags[i]) > 140:
                fileName = path + "/" + str(ids[i]) + tags[i][0:130] + "." + tmps[len(tmps) - 1]
            else:
                fileName=path+"/"+str(ids[i])+ tags[i]+"."+tmps[len(tmps)-1]
            urllib.request.urlretrieve("http:"+file_urls[i],fileName)
        except :
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
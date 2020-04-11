# -*- coding: UTF-8 -*-
# 初学者学习python的副产品
import requests                                 #网页
from scrapy.selector import Selector
import binascii                                 #转码
from tqdm import tqdm                           #进度条
import webbrowser                               #打开浏览器
import re                                       #正则表达式



def crc32asii(v):
    return '%x' % (binascii.crc32(v) & 0xffffffff)

def findUid(toBeFind , begin = 1 , end = 900000000 ):
    #穷举法逆向用户hash
    ans = []
    print("逆向中……")
    for i in tqdm(range( begin , end )):
        c = crc32asii(bytes(str(i), encoding='utf-8'))
        if(toBeFind == c):
            ans.append(i)
            print("找到：" + str(i) )
            if( input("极小可能哈希重值，是否继续? y/n :") != 'y' ):
                break
    return ans


def cid2hash(cid):
    t = ''
    url = 'https://api.bilibili.com/x/v1/dm/list.so?oid='+str(cid)
    body = requests.get(url).content
    xbody = Selector(text=str(body, encoding='utf-8'))
    lists = xbody.xpath("//d")

    for li in lists:
        content = li.xpath("./text()").get()
        par = li.xpath("./@p").get()
        pattern = re.compile(r'(?<=,0,)\w+(?=,)') 
        #正则表达式可能不严谨
        sentence = str(par)
        idHash = re.search(pattern, sentence )
        # idHash.group(0)提取搜索到的值
        text = 'hash: ' + str(idHash.group(0))+ " | " + str(content)+'\n' 
        t = t + text
    print(t)

def bvid2cid(bvid):
    # api来自 https://www.v2ex.com/t/655711
    url = 'https://danmu.u2sb.top/api/other/bilibili/queryaid/?bvid=' + str(bvid)
    urlReturn = requests.get(url)
    zidian = urlReturn.json()
    if(zidian['data'] == None):
        print('查无此BV!')
        return -1
    for i in zidian['data']['pageList']:
        print('cid:%10d  |  p%d %s'  % (i['cid'] , i['page'] , i['part']))
    return 0

def main():
    bvid = input("输入bv号:")
    while(bvid2cid(bvid) == -1):
        bvid = input("重新输入bv号:")
    cid = input("输入你选择的cid:")
    cid2hash(cid)
    yourHash = input("选择弹幕用户hash:")
    ans = findUid(yourHash)
    print("uid = " + str(ans))
    if(input("是否打开用户主页? y/n :") == 'y'):
        for i in ans:
            webbrowser.open("https://space.bilibili.com/" + str(i))
    return 0



if __name__ == '__main__':
    main()

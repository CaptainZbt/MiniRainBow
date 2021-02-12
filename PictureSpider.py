# -*- coding:UTF-8 -*-
import requests
from bs4 import BeautifulSoup
import re
import os
import time
import threading
import eventlet

def main(rootPath,headers,listUrl):
    # 创建本次爬虫存储根路径
    falg = os.path.exists(rootPath)
    if (falg == False):
        try:
            os.mkdir(rootPath)
            print("创建根目录成功，根目录：" + rootPath)
        except:
            print("创建文件夹失败，根目录已存在")

    # 获取列表页的内容,列表页的url  https://www.youwu333.com/x/1/list_1_1.html
    req = requests.get(listUrl)
    req.encoding = "utf-8"
    html = req.text

    # 获取列表页的各个写真集url
    reg = r'https://www\S+\.html'
    urlList = set(re.findall(reg, html))

    # 遍历列表页中的url
    for url in urlList:
        # 获取写真集的内容
        try:
            picReq = requests.get(url)
            print("获取网页内容成功，网页url：" + url)
        except:
            print("获取网页内容失败，网页url：" + url)
            continue
        picReq.encoding = "gbk"
        picConent = picReq.text

        # 获取写真名称
        bf = BeautifulSoup(picConent)
        picTitle = bf.head.title.string

        # 创建该写真存储的本地文件夹
        dirpath = rootPath + "\\" + picTitle
        falg = os.path.exists(dirpath)
        if (falg == False):
            try:
                os.mkdir(dirpath)
                print("创建写真文件夹成功，文件夹名：" + dirpath)
            except:
                print("创建写真文件夹失败，文件夹已存在，文件夹名：" + dirpath)
                continue
        # 获取当前页面中的图片
        jpgReg = r'https://pic\S+\.jpg'
        picUrlList = re.findall(jpgReg, picConent)

        # 从html内容中获取各个分类页的url
        otherReg = r'href=\'\d\S+\.html'
        otherIndexList = set(re.findall(otherReg, picConent))
        # 从各个分类页中获取图片的url，然后累加到图片的list中
        for otherIndex in otherIndexList:
            # 截取拼接url字符串
            indexStr = otherIndex.replace("href=\'", "")
            replaceStr = indexStr.split("_")[0]
            endStr = indexStr.split(".")[0]
            otherUrl = url.replace(replaceStr, endStr)

            # 获取各个图片的url，累加一起
            try:
                otherPicReq = requests.get(otherUrl)
                print("获取网页内容成功，网页url：" + otherUrl)
            except:
                print("获取网页内容失败，网页url：" + otherUrl)
                continue
            otherPicReq.encoding = "gbk"
            otherPicConent = otherPicReq.text
            otherPicList = re.findall(jpgReg, otherPicConent)
            picUrlList.extend(otherPicList)

        # 遍历图片url,开始下载图片
        x = 0
        for imageUrl in picUrlList:
            path = dirpath + "\\" + str(x) + ".jpg"
            print(path)
            print(imageUrl)
            eventlet.monkey_patch()  # 必须加这条代码
            with eventlet.Timeout(5, False):  # 设置超时时间为2秒
                try:
                    img = requests.get(imageUrl, headers=headers).content
                    with open(path, 'wb') as f:
                        f.write(img)
                        print("正在下载{}第{}张图片".format(picTitle, x))
                except:
                    print('{}第{}张图片下载失败'.format(picTitle, x))
            x += 1
            time.sleep(0.5)
        break


if __name__ == "__main__":
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36 Edg/87.0.664.75'
    }
    rootPath = "C:\\迅雷下载\\爬虫1028"
    listUrl="https://www.youwu333.com/x/1/list_1_1.html"
    main(rootPath,headers,listUrl)















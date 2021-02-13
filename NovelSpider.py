# -*- coding:UTF-8 -*-
import requests
from bs4 import BeautifulSoup
import re
import os
import time
import eventlet

def main(rootPath,listUrl):
    # 创建本次爬虫存储根路径
    falg = os.path.exists(rootPath)
    if (falg == False):
        try:
            os.mkdir(rootPath)
            print("创建根目录成功，根目录：" + rootPath)
        except:
            print("创建文件夹失败，根目录已存在")

    # 获取首页的内容
    req = requests.get(listUrl)
    req.encoding = "gbk"
    html = req.text
    # 获取各个分类页面的url
    reg1 = r'/book\d\S+\d/'
    urlList = set(re.findall(reg1, html))

    # 遍历分类页中的url
    for index in urlList:
        tempurl="https://www.duquanben.com"+index
        # 获取分类页中的内容
        try:
            novelClassReq = requests.get(tempurl)
            print("获取分类页网页内容成功，网页url：" + tempurl)
        except:
            print("获取分类页网页内容失败，网页url：" + tempurl)
            continue
        novelClassReq.encoding = "gbk"
        classListConent = novelClassReq.text
        # 获取分类页所有子页的url
        bf = BeautifulSoup(classListConent)
        lastCon = bf.findAll(class_="last")
        lastStr = "".join([str(x) for x in lastCon])
        maxNum = lastStr.split(">")[1].split("<")[0]

        childUrl=[]
        for i in range(1,2):#int(maxNum)
            endStr = "/" + index.split("/")[1] + "/" + index.split("/")[2] + "/" + str(i) + "/"
            url = "https://www.duquanben.com" + endStr
            childUrl.append(url)

        bookUrls=[]
        # 遍历每一个子页
        for childurl in childUrl:
            # 获取子页中的内容
            try:
                childContentReq = requests.get(childurl)
                print("获取子页内容成功，网页url：" + childurl)
            except:
                print("获取子页内容失败，网页url：" + childurl)
                continue
            childContentReq.encoding = "gbk"
            childContent = childContentReq.text
            # 获取子页中的每个书的url
            bookreg = r'https://www.duquanben.com/xiaoshuo\S+\d/'
            bookUrl = set(re.findall(bookreg, childContent))
            bookUrls.extend(bookUrl)

        # 遍历每一本书的url
        for bookurl in bookUrls:
            # 获取书中的章节内容
            try:
                bookChapterReq = requests.get(bookurl)
                print("获取书的章节内容成功，网页url：" + bookurl)
            except:
                print("获取书的章节内容失败，网页url：" + bookurl)
                continue
            bookChapterReq.encoding = "gbk"
            chapterContent = bookChapterReq.text

            # 获取书名
            bookBF = BeautifulSoup(chapterContent)
            bookName = bookBF.head.title.string.split("_")[0].replace("全文阅读","")
            # 获取每一本书的所有章节目录的url
            chapterReg = r'href="\d\S+\d.html'
            chaUrlList = set(re.findall(chapterReg, chapterContent))
            # 按照书名创建文件夹
            bookPath=rootPath+"\\"+bookName
            bookfalg = os.path.exists(bookPath)
            if (bookfalg == False):
                try:
                    os.mkdir(bookPath)
                    print("创建小说目录成功，小说目录：" + bookPath)
                except:
                    print("创建文件夹失败，小说目录已存在")

            # 遍历每一个章节目录的url
            for chapterurl in chaUrlList:
                chapterUrl=bookurl+chapterurl.replace("href=\"","")
                # 获取章节中的内容
                try:
                    contentReq = requests.get(chapterUrl)
                    print("获取章节中正文内容成功，网页url：" + chapterUrl)
                except:
                    print("获取章节中正文内容失败，网页url：" + chapterUrl)
                    continue
                contentReq.encoding = "gbk"
                contenthtml = contentReq.text

                # 获取章节中的章节名
                contentBF = BeautifulSoup(contenthtml)
                ChapterName = contentBF.head.title.string.split("_")[0]
                # 获取章节中的正文
                content=contentBF.find('div',id='htmlContent',class_='contentbox').text.split("\n")[1]
                #将内容记录到文本中
                eventlet.monkey_patch()
                with eventlet.Timeout(5, False):  # 设置超时时间为5秒，每个章节下载时长不超过5s，否则超时退出
                    try:
                        chapterPath=bookPath+"\\"+ChapterName+".txt"
                        with open(chapterPath, 'a', encoding='utf-8') as f:
                            f.write(ChapterName + '\n')  # 写入名字并换行
                            f.writelines(content)  # 追加内容
                            f.write('\n\n')  # 换两行
                            print("创建章节文件成功，文件名:"+chapterPath)
                    except:
                        print("创建章节文件失败，文件名:"+chapterPath)
                time.sleep(0.5)

if __name__ == "__main__":
    rootPath = "C:\\迅雷下载\\爬虫1028"
    listUrl="https://www.duquanben.com/"
    main(rootPath,listUrl)















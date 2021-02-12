# coding: utf-8
from concurrent.futures import ThreadPoolExecutor
import time
import PictureSpider

def main():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36 Edg/87.0.664.75'
    }
    rootPath = "C:\\迅雷下载\\爬虫1028"
    listUrl = "https://www.youwu333.com/x/1/list_1_1.html"
    with ThreadPoolExecutor(max_workers=8) as t:
        for i in range(10):
            endStr="_1_"+str(i)
            url=listUrl.replace("_1_1",endStr)
            t.submit(PictureSpider.main(rootPath,headers,url))


if __name__ == "__main__":
    main()
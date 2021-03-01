# coding: utf-8
from concurrent.futures import ThreadPoolExecutor
from com.rainbow.spider import PictureSpider
import configparser
import os
import codecs
import logging

class entrance:
    def __init__(self,path):
        self.path=path
        root_dir = os.path.dirname(os.path.abspath('.'))
        cf = configparser.ConfigParser()
        cf.readfp(codecs.open(root_dir + "\\" + self.path + "\\config.ini", "r", "utf-8-sig"))
        self.rootPath = cf.get("PICTURE", "rootPath")
        self.listUrl = cf.get("PICTURE", "listUrl")
        self.timeout = float(cf.get("PICTURE", "timeout"))
        self.sleepTime = float(cf.get("PICTURE", "sleepTime"))
        self.headers = cf.get("PICTURE", "headers")
        LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
        DATE_FORMAT = "%m/%d/%Y %H:%M:%S %p"
        logging.basicConfig(filename=self.rootPath + "\\pictureSpider.log", level=logging.DEBUG, format=LOG_FORMAT,
                            datefmt=DATE_FORMAT)

    def main(self):
        with ThreadPoolExecutor(max_workers=8) as t:
            for i in range(10):
                endStr="_1_"+str(i)
                url=self.listUrl.replace("_1_1",endStr)
                t.submit(PictureSpider.picture(self.headers,url,self.rootPath,self.timeout,self.sleepTime).main())

if __name__== "__main__" :
    entrance("spider").main()

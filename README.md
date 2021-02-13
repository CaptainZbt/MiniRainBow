# MiniRainBow  
爬取公网的各种资源,当前仅限于图片和小说  

GIT CLONE 命令：  
git clone https://github.com/CaptainZbt/MiniRainBow.git

爬虫中的请求头：  
header参数需要根据自己的header设置，具体怎么获取，可以百度  

多线程：  
受限于个人电脑的电脑核心数量，总的线程数不会太多，所以代码中的8个线程数，会申请不到，但也不需要更改； 

使用：  
1.前提：需要python环境，以及其中的依赖  
2.文件：将代码放到用一个目录下  
3.在cmd窗口中,执行命令：
```
图片写真：python SpiderMain.py   
小说下载：python NovelSpider.py  
```

版本：V0.1   
提示：当前初始阶段，继续优化中  
仅限于图片：https://www.youwu333.com/  
仅限于小说：https://www.duquanben.com/  

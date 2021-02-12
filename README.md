# RainBowData
爬取公网的各种资源

GIT配置：
https://blog.csdn.net/liuweixiao520/article/details/78971221
https://www.cnblogs.com/jf-67/p/6415637.html
https://www.cnblogs.com/kesz/p/10921987.html

爬虫中的请求头：
header参数需要根据自己的header设置，具体怎么获取，可以百度

多线程：
受限于个人电脑的电脑核心数量，总的线程数不会太多，所以代码中的8个线程数，会申请不到，但也不需要更改；

使用：
1.前提：需要python环境，以及其中的依赖
2.文件：将代码放到用一个目录下
3.在cmd窗口中,执行命令：python SpiderMain.py 
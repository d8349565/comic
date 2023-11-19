# gunicorn -c run.py app:app
# pstree -ap | grep gunicorn
import os
bind = '0.0.0.0:8812'      #绑定ip和端口号
backlog = 512                #监听队列
timeout = 30      #超时
chdir = os.path.abspath(os.path.dirname(__file__)) #gunicorn要切换到的目的工作目录
workers = 1
threads = 2 #指定每个进程开启的线程数
# worker_class = 'gevent'
# worker_connections = 1000

daemon = True # 是否以守护进程启动，默认false；

loglevel = 'info' #日志级别，这个日志级别指的是错误日志的级别，而访问日志的级别无法设置
access_log_format = '%(t)s %(p)s %(h)s "%(r)s" %(s)s %(L)s %(b)s %(f)s" "%(a)s"'    #设置gunicorn访问日志格式，错误日志无法设置
accesslog = "gunicorn_access.log"      #访问日志文件
errorlog = "gunicorn_error.log"        #错误日志文件
capture_output = True # 捕捉打印输出内容
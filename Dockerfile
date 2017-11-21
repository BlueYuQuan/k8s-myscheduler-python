#This Dockerfile uses to test the my python scheruldr progrem for k8s 
#VERSION 1.0
#ImageName: sjq-python-scheduler
#Author: songjinquan

#基于基础镜像
FROM registry.cn-hangzhou.aliyuncs.com/sjq-study/python:3.6
#维护者
MAINTAINER 441452752@qq.com
#为3.6安装pip
RUN wget https://bootstrap.pypa.io/get-pip.py
RUN python3.6 get-pip.py
#print()时在控制台正常显示中文
ENV PYTHONIOENCODING=utf-8
#将当前目录下的文件全部复制到基础镜像的/usr/src/myapp目录下
COPY . /usr/src/myapp
#为后续的RUN,CMD,ENTRYPOINT指令配置工作目录
WORKDIR /usr/src/myapp
#下载需要的依赖
RUN pip3 install -r requirements.txt
#指定启动容器时执行的命令--启动程序
CMD ["python", "k8s-my-scheduler-code_test.py"]

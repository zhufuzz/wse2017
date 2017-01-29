# -*- coding:utf-8 -*-   x
#os模块
import os

#获取操作系统平台
print os.name

#获取工作目录
print os.getcwd()

#获取某个目录下的所有文件名
#print os.listdir("c:/python27")

#运行一个shell命令
#os.system("calc")

#删除某个文件
#os.remove("G:/文件操作演示文件夹/a.mp3")

#判断一个地方是文件夹还是文件
#print os.path.isfile("G:/文件操作演示文件夹/a.mp8")
#print os.path.isdir("G:/文件操作演示文件夹")

#把一个路径拆分为目录+文件名的形式。
print os.path.split("C:/python27/a.mp8")
print os.path.split("C:/python27")
print os.path.split("C:/python27/")

# -*- coding:utf-8 -*-   x
#远程控制开关机项目

#软件工程中，一般对于这种项目会按模块的思路去做，一个模块负责一项或多项特定功能，各模块之间通过接口进行设计，在此模块
#指的是这里的函数，现在所说的软件工程中“模块”概念与Python中“模块”概念是有区别的。
#先看模块划分
def guanji():
    a=1
    #此函数负责发送关机的标题（即guan）给邮箱
def chongqi():
    a=1
    #此函数负责发送重启（即chong）的标题给邮箱
def read():
    a=1
    #此函数负责读取邮件中的指令，指令为guan返回0，指令为chong返回1
if __name__ == '__main__':  #当运行此程序的时候，读取邮件
    if read== 0:
        os.system('shutdown -s -t 1')
        
    if read== 1:    
        os.system('shutdown -r')

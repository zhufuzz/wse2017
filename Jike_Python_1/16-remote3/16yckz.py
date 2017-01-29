#远程控制开关机项目
import time
import os
import sys
import poplib
import smtplib
from email.header import decode_header
from email.mime.text import MIMEText
import email

def guanji():
    #此函数负责发送关机的标题（即guan）给邮箱
    sent=smtplib.SMTP('smtp.sina.com') 
    sent.login('weiweihappy321@sina.com','aA123456789')
    to=['weiweihappy321@sina.com']
    content = MIMEText('')
    content['Subject']='guan'
    content['From']='weiweihappy321@sina.com'
    content['To']=','.join(to)
    sent.sendmail('weiweihappy321@sina.com',to,content.as_string())
    sent.close()

def chongqi():
    #此函数负责发送重启（即chong）的标题给邮箱
    sent=smtplib.SMTP('smtp.sina.com') 
    sent.login('weiweihappy321@sina.com','aA123456789')
    to=['weiweihappy321@sina.com']
    content = MIMEText('')
    content['Subject']='chong'
    content['From']='weiweihappy321@sina.com'
    content['To']=','.join(to)
    sent.sendmail('weiweihappy321@sina.com',to,content.as_string())
    sent.close()


def read():
    #此函数负责读取邮件中的指令，指令为guan返回0，指令为chong返回1
    read=poplib.POP3('pop.sina.com')
    read.user('weiweihappy321@sina.com')
    read.pass_('aA123456789')
    tongji=read.stat()#返回邮箱基本统计信息
    str = read.top(tongji[0], 0)  #返回最近的邮件信息
    str2=[]
    for x in str[1] : #编码与解码
                try:  
                    str2.append(x.decode())  
                except:  
                    try:  
                        str2.append(x.decode('gbk'))  
                    except:  
                        str2.append((x.decode('big5')))
    msg = email.message_from_string('\n'.join(str2))#把String的邮件转换成email.message实例  
    biaoti = decode_header(msg['subject'])
    if biaoti[0][1]:   #如果有第二个元素，说明有编码信息
           biaoti2 = biaoti[0][0].decode(biaoti[0][1])  
    else:  
           biaoti2= biaoti[0][0]
    #OK,此时成功获取到最近一封邮件标题，即biaoti2
    if biaoti2=="guan":
        return 0
    if biaoti2=="chong":
        return 1
    read.quit()

if __name__ == '__main__':  #当运行此程序的时候，读取邮件
    while True:
        time.sleep(2)
        if read()==0:
            os.system('shutdown -s -t 10')
            break
        if read()== 1:    
            os.system('shutdown -r')
            break


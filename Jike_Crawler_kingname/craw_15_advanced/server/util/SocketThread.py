#-*-coding:utf8-*-

import json
import threading
import time

class SocketThread(threading.Thread):
    BUFFER_SIZE = 2048*100      # 读取数据大小
    def __init__(self, conn=None, ip=None, socketPool=None):
        threading.Thread.__init__(self)
        print u'生成一个socket， ip地址为: %s' % str(ip)
        self.conn = conn
        self.ip = ip
        self.socketPool = socketPool
        self.lock = threading.Lock()
        self.masterSocket = None

    def getIp(self):
        return self.ip

    def sendToMaster(self, message, advancedFunction=''):
        print u'给控制端返回信息： %s' % message
        if not advancedFunction:
            self.conn.sendall(self.generateReturn(message))
        else:
            self.conn.sendall(self.generateReturn(message, advancedFunction))

    def run(self):
        while True:
            # 读取数据，数据还没到来阻塞
            try:
                data = self.conn.recv(self.BUFFER_SIZE)
                if len(data):
                    self.analysisCommand(data)
                else:
                    print u'对方关闭Socket。'
                    self.lock.acquire()
                    if self.ip in self.socketPool:
                        self.socketPool.pop(self.ip)
                        print 'pop1'
                        print self.socketPool
                    self.lock.release()
                    break
            except Exception, e:
                print u'socket 连接中断。'
                self.lock.acquire()
                if self.ip in self.socketPool:
                    self.socketPool.pop(self.ip)
                    print 'pop2'
                self.lock.release()
                break
            print 'shit'

    def analysisCommand(self, command):
        u'''
        {"from":"master", "to": "xx.xx.xx.xx", "type": "commandInConfig", "command": "xxxx"}
        to的值可能是空，表示在服务器执行，会在是具体IP地址
        {"from":"slave", "info":"xxxx"}

        '''
        print '=================分析命令================='
        print str(command)
        try:
            if '#finished#' in command:
                command = command[:-10]
            print u'命令为： %s' % command
            commandDict = json.loads(command)
        except Exception, e:
            print u'命令格式有问题：%s' % str(e)

        if commandDict:
            commandFrom = commandDict['from']
            if commandFrom == 'master':
                #下面这一行用来解决第二次课遇到的问题
                masterSocket = self.socketPool.pop(self.ip)
                self.lock.acquire()
                self.socketPool['master'] = masterSocket
                self.lock.release()
                result = self.analysisMasterCommand(commandDict['type'], commandDict['to'], commandDict['command'])
                print u'分析结果为：%s' % result
                self.sendToMaster(result, commandDict['type'])
            elif commandFrom == 'slave':
                if 'http' in commandDict['info']: #这种判断方法显然是不完备的，如果复制的内容正好含有http就会出问题，请同学想办法修正
                    returnInfo = json.dumps({'printScreen': commandDict['info']})
                else:
                    returnInfo = json.dumps({'copyResult': commandDict['info']})
                print returnInfo
                self.socketPool['master'].send(returnInfo + '#finished#')
                time.sleep(5)

    def getSlaveList(self):
        self.lock.acquire()
        slaveList = self.socketPool.keys()
        self.lock.release()
        return slaveList

    def generateToSlaveMessage(self, message, commandType):
        return json.dumps({'command': message, 'type': commandType}) + '#finished#'

    def sendToSlave(self, slaveSocketThread, message, commandType):
        toSlaveMessage = self.generateToSlaveMessage(message, commandType)
        print u'以下命令将会被发送给被控端: %s' % toSlaveMessage
        try:
            slaveSocketThread.send(toSlaveMessage)
        except Exception, e:
            print u'向被控端发送数据出错：%s' % str(e)
            return ''

        if commandType == 'advancedFunction':
            if message == 'copyClipboard' or 'printScreen':
                raise Exception #抛出一个错误来杀死这个子线程，以避免它给控制端发信息。

    def generateReturn(self, info, advancedFunction=''):
        if not advancedFunction:
            returnInfo = {'slaveList': info}
        elif advancedFunction == 'copyResult':
            returnInfo = {'copyResult': info}
        elif advancedFunction == 'printScreen':
            returnInfo = {'printScreen': info}
        else:
            returnInfo = {}
        returnInfo = json.dumps(returnInfo)
        returnInfo = returnInfo + '#finished#'
        print u'以下内容将会返回给控制端: %s' % returnInfo
        return returnInfo

    def analysisMasterCommand(self, commandType, to, command):
        if not to:
            print u'这条命令在服务器上执行， 命令是%s' % command
            if command == 'listSlave':
                return self.getSlaveList()
        print u'这条命令将会在%s上面执行，命令的类型是%s, 命令的内容是:%s' % (to, commandType, command)
        if to not in self.socketPool:
            print u'找不到ip地址为%s的被控端' % to
            return ''
        else:
            result = self.sendToSlave(self.socketPool[to], command, commandType)
        return result

    def send(self, info):
        self.lock.acquire()
        self.conn.sendall(info)
        self.lock.release()

    def receive(self, buffers):
        self.conn.recv(buffers)

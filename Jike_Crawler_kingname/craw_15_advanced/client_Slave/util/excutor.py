#-*-coding:utf8-*-

import os
import win32api
from mccLog import mccLog
from ScreenShotter import ScreenShotter
from ClipboardHelper import ClipboardHelper

class executor(object):
    def __init__(self, commandDict, openDict):
        self.mccLog = mccLog()
        self.commandDict = commandDict
        self.openDict = openDict

    def execute(self, commandType, command):
        self.mccLog.mccWriteLog(u'开始处理命令。')
        if not commandType == 'advancedFunction':
            if commandType == 'commandInConfig':
                self.exeInnerCommand(command)
            elif commandType == 'commandInWrite':
                self.exeWriteCommand(command)
            return ''
        else:
            if command == 'copyClipboard':
                return self.readClipboard()
            elif command == 'printScreen':
                return self.printScreen()

    def exeInnerCommand(self, innerCommand):
        if innerCommand in self.commandDict:
            self.mccLog.mccWriteLog(u'执行命令')
            try:
                command = self.commandDict[innerCommand]
                os.system(command)
                self.mccLog.mccWriteLog(u'执行命令成功')
            except Exception, e:
                self.mccLog.mccError(u'执行命令失败' + str(e))
        elif innerCommand in self.openDict:
            self.mccLog.mccWriteLog(u'打开文件')
            try:
                openFile = self.openDict[innerCommand]
                win32api.ShellExecute(0, 'open', openFile, '', '', 1)
                self.mccLog.mccWriteLog(u'打开文件成功')
            except Exception, e:
                self.mccLog.mccError(u'打开文件失败：' + str(e))
        else:
            self.mccLog.mccError(u'命令%s不存在！' % innerCommand)

    def exeWriteCommand(self, writeCommand):
            if writeCommand:
                self.sandBox(writeCommand)

    def sandBox(self, code):
        u'''
        注意：提交的代码请不要出现中文或者中文字符，否则会报错。
        '''
        with open('writeCommand.py', 'w') as f:
            f.write(code)
        os.system('python ' + 'writeCommand.py')

    def printScreen(self):
        try:
            print u'开始截屏'
            result = ScreenShotter().upload()
            return result

        except Exception, e:
            print 'upload screenshots error: %s' % str(e)
            return ''

    def readClipboard(self):
        try:
            result = ClipboardHelper.read()
            print 'clipboard result is: %s' % result
            return result
        except Exception, e:
            return ''

    def writeClipboard(self, text):
        ClipboardHelper.write(text)

#-*-coding:utf8-*-
from PIL import ImageGrab
import time
import shlex
import subprocess

class ScreenShotter:
    AK = '7rTZOc8Z7vml782tMOyIMWad90WHZZtnjHTgzMUi'
    SK = 'VfLpvljTh2VbNYRwjC_zxbReHfcftKLIlV1uM3Cs'
    CHECK_ACCOUNT = 'qshell.exe account'
    ACCOUNT_INIT = 'qshell.exe account %s %s' % (AK, SK)
    UPLOAD_COMMAND = 'qshell.exe fput picturebed %s %s true'
    PIC_URL = 'http://7sbpmp.com1.z0.glb.clouddn.com/%s'

    def __init__(self):
        self.initAccount()

    def initAccount(self):
        account = subprocess.Popen(shlex.split(self.CHECK_ACCOUNT), stdout=subprocess.PIPE)
        out = account.communicate()
        print out
        if 'Open account file failed' in out[0]:
            out = subprocess.Popen(shlex.split(self.ACCOUNT_INIT), stdout=subprocess.PIPE)
            print out.communicate()

    def printScreen(self):
        print u'开始截图'
        try:
            pic = ImageGrab.grab()
            pic.save('screenshots.jpg')
            return True
        except Exception, e:
            return False

    def calcNowTime(self):
        return time.strftime('%Y-%m-%d-%H-%H-%S', time.localtime(time.time()))

    def upload(self):
        print u'准备上传文件'
        self.printScreen()
        time.sleep(1)
        fileName = 'jikexueyuan' + self.calcNowTime() + '.jpg'
        print u'文件名为 %s' % fileName
        result = subprocess.Popen(shlex.split(self.UPLOAD_COMMAND % (fileName, 'screenshots.jpg')), stdout=subprocess.PIPE)
        resultStr = result.communicate()
        print resultStr
        return self.PIC_URL % fileName

if __name__ == '__main__':
    print ScreenShotter().upload()

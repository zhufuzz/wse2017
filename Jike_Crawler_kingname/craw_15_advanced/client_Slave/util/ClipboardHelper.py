#-*-coding:utf8-*-
import win32con
import win32clipboard as clipboard

class ClipboardHelper:
    '''
    如果复制的内容里面含有中文或者中文字符的话，最后得到的结果是乱码，这是由于Python2对
    中文编码的支持不完善造成的。对于这个问题，我建议各位同学转到Python3, 这是最简单的
    解决办法。我以后的课程也会使用Python3，Python2应该渐渐退出历史舞台了。--kingname
    '''
    def __init__(self):
        pass

    @staticmethod
    def read():
        clipboard.OpenClipboard()
        data = clipboard.GetClipboardData(win32con.CF_TEXT)
        clipboard.CloseClipboard()
        return data

    @staticmethod
    def write(text):
        clipboard.OpenClipboard()
        clipboard.EmptyClipboard()
        clipboard.SetClipboardData(win32con.CF_TEXT, text)
        clipboard.CloseClipboard()

if __name__ == '__main__':
    clipboardHelper = ClipboardHelper()
    print clipboardHelper.read()
    clipboardHelper.write('jikexueyuan')

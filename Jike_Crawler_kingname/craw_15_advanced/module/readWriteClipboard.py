import win32con
import win32clipboard as clipboard

class ClipboardHelper:
    def __init__(self):
        pass

    def read(self):
        clipboard.OpenClipboard()
        data = clipboard.GetClipboardData(win32con.CF_TEXT)
        print data
        clipboard.CloseClipboard()

    def write(self, text):
        clipboard.OpenClipboard()
        clipboard.EmptyClipboard()
        clipboard.SetClipboardData(win32con.CF_TEXT, text)
        clipboard.CloseClipboard()

if __name__ == '__main__':
    clipboardHelper = ClipboardHelper()
    print clipboardHelper.read()
    clipboardHelper.write('jikexueyuan')

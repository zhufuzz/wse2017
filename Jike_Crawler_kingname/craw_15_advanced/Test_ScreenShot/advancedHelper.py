#-*-coding:utf8-*-
import ctypes
import win32api
from ctypes.wintypes import *
import win32clipboard
from win32con import *
import win32con
import sys
import time

class BITMAPFILEHEADER(ctypes.Structure):
    _pack_ = 1  # structure field byte alignment
    _fields_ = [
        ('bfType', WORD),  # file type ("BM")
        ('bfSize', DWORD),  # file size in bytes
        ('bfReserved1', WORD),  # must be zero
        ('bfReserved2', WORD),  # must be zero
        ('bfOffBits', DWORD),  # byte offset to the pixel array
    ]

class BITMAPINFOHEADER(ctypes.Structure):
    _pack_ = 1  # structure field byte alignment
    _fields_ = [
        ('biSize', DWORD),
        ('biWidth', LONG),
        ('biHeight', LONG),
        ('biPLanes', WORD),
        ('biBitCount', WORD),
        ('biCompression', DWORD),
        ('biSizeImage', DWORD),
        ('biXPelsPerMeter', LONG),
        ('biYPelsPerMeter', LONG),
        ('biClrUsed', DWORD),
        ('biClrImportant', DWORD)
    ]

class ScreenShotter:
    SIZEOF_BITMAPFILEHEADER = ctypes.sizeof(BITMAPFILEHEADER)
    SIZEOF_BITMAPINFOHEADER = ctypes.sizeof(BITMAPINFOHEADER)

    def __init__(self):
        pass

    def printScreen(self):
        win32api.keybd_event(win32con.VK_SNAPSHOT, 0, 0, 0)
        win32api.keybd_event(win32con.VK_SNAPSHOT, 0, KEYEVENTF_KEYUP, 0)
        time.sleep(1)

    def saveImg(self):
        win32clipboard.OpenClipboard()
        try:
            if win32clipboard.IsClipboardFormatAvailable(win32clipboard.CF_DIB):
                data = win32clipboard.GetClipboardData(win32clipboard.CF_DIB)
            else:
                print('clipboard does not contain an image in DIB format')
                sys.exit(1)
        finally:
            win32clipboard.CloseClipboard()

        bmih = BITMAPINFOHEADER()
        ctypes.memmove(ctypes.pointer(bmih), data, self.SIZEOF_BITMAPINFOHEADER)

        if bmih.biCompression != BI_BITFIELDS:  # RGBA?
            print('insupported compression type {}'.format(bmih.biCompression))
            sys.exit(1)

        bmfh = BITMAPFILEHEADER()
        ctypes.memset(ctypes.pointer(bmfh), 0, self.SIZEOF_BITMAPFILEHEADER)  # zero structure
        bmfh.bfType = ord('B') | (ord('M') << 8)
        bmfh.bfSize = self.SIZEOF_BITMAPFILEHEADER + len(data)  # file size
        SIZEOF_COLORTABLE = 0
        bmfh.bfOffBits = self.SIZEOF_BITMAPFILEHEADER + self.SIZEOF_BITMAPINFOHEADER + SIZEOF_COLORTABLE

        bmp_filename = 'clipboard.bmp'
        print bmp_filename
        with open(bmp_filename, 'wb') as bmp_file:
            bmp_file.write(bmfh)
            bmp_file.write(data)

        print('file "{}" created from clipboard image'.format(bmp_filename))

if __name__ == '__main__':
    screenShotter = ScreenShotter()
    screenShotter.printScreen()
    screenShotter.saveImg()





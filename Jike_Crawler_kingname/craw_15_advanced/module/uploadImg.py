import requests
import os
# imgName = '2.jpg'
# url = 'http://127.0.0.1:5000'
# f = {'file': open(imgName, 'rb')}
# url = requests.post(url, files=f).content
# print url

AK = '7rTZOc8Z2vml785tMOyIsWaV90WHZ2tnjHTgzMUi'
SK = 'VfLpvljTh5VbNYvwjC_zxbReHDsftKLIlV1uM3Cs'
command = 'qshell\\qshell.exe account %s %s' % (AK, SK)
os.system(command)
command = 'qshell\\qshell.exe fput picturebed %s %s true' % ('jikexueyuan333.jpg', '2.jpg')
os.system(command)
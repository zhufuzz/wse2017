import subprocess
import os
import time
# os.system('ping www.baidu.com')

# a = subprocess.Popen('dir', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
#
# b = a.stdout.readlines()
# for i in b:
#     print i

while True:
    f = open('conf.txt', 'r')
    content = f.read()
    os.system(content)
    time.sleep(5)
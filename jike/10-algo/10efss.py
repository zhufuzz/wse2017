# -*- coding:utf-8 -*-   x
def efss(arr, x):
  i= 0
  j= len(arr) - 1
  for k in range(j/2 + 1):
    if i>j:
        print -1
    zj= (i+j)/2    #中间位置为i+j的和除以2
    if arr[zj]==x:
      return zj
    elif arr[zj]>x:
      j= zj-1
    else:
      i= zj+ 1

# -*- coding:utf-8 -*-   x
#快排的实现


def kp(arr,i,j):    #快排总调用函数
     if i < j:
        base = kpgc(arr,i,j)
        kp(arr,i,base)
        kp(arr,base+1,j)

def kpgc(arr,i,j):    #快排排序过程
    base = arr[i]
    while i < j:
        while i < j and arr[j] >= base:
            j -= 1
        while i < j and arr[j] < base:
            arr[i] = arr[j]
            i += 1
            arr[j] = arr[i]
    arr[i] = base
    return i


arr=[2,55,4,34,67,75,9]
kp(arr,0, len(arr)-1)
print arr
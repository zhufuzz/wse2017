# -*- coding:utf-8 -*-   x
#选择排序的实现
def xzpx(arr):    #选择排序
    for i in range(0, len (arr)): #每一趟排序
        k= i
        for j in range(i + 1, len(arr)): #每一趟选择最小的这个数
            if arr[j] < arr[k]:
                k= j
        arr[i], arr[k] = arr[k], arr[i]       #交换位置


arr=[2,55,4,34,67,75,9]
xzpx(arr)
print arr
 # -*- coding: utf-8 -*-
"""
Created on Sun Nov  4 10:56:20 2018

@author: YeZhiFei
"""
import os
import sys
from collections import Counter
import numpy as np

base_dir = 'data'
train_dir = os.path.join(base_dir, 'train.txt')

if sys.version_info[0] > 2:
    is_py3 = True
else:
    reload(sys)
    sys.setdefaultencoding("utf-8")
    is_py3 = False
    
def open_file(filename, mode='r'):
    """
    常用文件操作，可在python2和python3间切换.
    mode: 'r' or 'w' for read or write
    """
    if is_py3:
        return open(filename, mode, encoding='utf-8', errors='ignore')
    else:
        return open(filename, mode)


def read_file(filename):
    """读取文件数据"""
    contents = []
    red_bolls = []
    sum1=[]
    sum2=[]
    sum3=[]
    with open_file(filename) as f:
        for line in f:
            try:
                info = line.strip().split('\t')
                contents.append(info)
                a=0
                b=0
                c=0
                for i in range(1,7):
                    if int(info[i])<=10:
                        a=a+1
                    if int(info[i])>10 and int(info[i])<=20:
                        b=b+1
                    if int(info[i])>20:
                        c=c+1
                    red_bolls.append(info[i])
                sum1.append(a)
                sum2.append(b)
                sum3.append(c)
            except:
                pass
    return contents,red_bolls,sum1,sum2,sum3
def caculate_avg(data):
    sum_data=0
    for item in data:
        sum_data=sum_data+item
    avg=sum_data/len(data)
    return avg

contents,red_bolls,sum1,sum2,sum3=read_file(train_dir)
counter = Counter(red_bolls)
print(len(sum1))
print(len(sum2))
print(len(sum3))
#红球
#for k,v in counter.items():
#    print(k,v)
for i in range(1,35):
    print("%s,%s"%(i,counter[str(i)]))
#蓝球
items=[]
for item in contents:
    items.append(item[7])
counter1 = Counter(items)
for i in range(1,35):
    print("%s,%s"%(i,counter1[str(i)]))
#各个区间球的个数
avg1=caculate_avg(sum1)
avg2=caculate_avg(sum2)
avg3=caculate_avg(sum3)
#统计各个区间出现次数
counter_sum1 = Counter(sum1)
print(counter_sum1)

counter_sum2 = Counter(sum2)
print(counter_sum2)

counter_sum3 = Counter(sum3)
print(counter_sum3)


    
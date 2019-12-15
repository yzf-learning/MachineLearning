# -*- coding: utf-8 -*-
"""
Created on Sun Feb 24 12:29:19 2019

@author: Administrator
"""

import numpy as np
a = np.random.rand(1)*12
print(a)
b = [1,2,4]
c = np.searchsorted([1,2,4],a,side='right')
print(c)


data1=[1,2,2,2,4,6]
data_all=[1,2, 2,  2,  4,  6,  0,  3,  4,  5,  5, 18]
cdf1 = np.searchsorted(data1,data_all,side='right')

cdf1
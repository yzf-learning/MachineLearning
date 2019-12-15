# -*- coding: utf-8 -*-
"""
Spyder Editor
KS的计算步骤如下：

计算每个评分区间的好坏账户数（计算的是特征的KS的话，是每个特征对应的好坏账户数）。
计算每个评分区间的累计好账户数占总好账户数比率(good%)和累计坏账户数占总坏账户数比率(bad%)。
计算每个评分区间累计坏账户占比与累计好账户占比差的绝对值（累计good%-累计bad%），然后对这些绝对值取最大值即得此评分卡的KS值。
This is a temporary script file.
"""
import pandas as pd
import numpy as np

def ks_calc_2samp(data,score_col,class_col):
    '''
    功能: 计算KS值，输出对应分割点和累计分布函数曲线图
    输入值:
    data: 二维数组或dataframe，包括模型得分和真实的标签
    score_col: 一维数组或series，代表模型得分（一般为预测正类的概率）
    class_col: 一维数组或series，代表真实的标签（{0,1}或{-1,1}）
    输出值:
    'ks': KS值，'cdf_df': 好坏人累积概率分布以及其差值gap
    '''
    Bad = data.ix[data[class_col[0]]==1,score_col[0]]
    Good = data.ix[data[class_col[0]]==0, score_col[0]]
    data1 = Bad.values
    data2 = Good.values
    n1 = data1.shape[0]
    n2 = data2.shape[0]
    data1 = np.sort(data1)
    data2 = np.sort(data2)
    print(data1)
    print(data2)
    data_all = np.concatenate([data1,data2])
    print(data_all)
    cdf1 = np.searchsorted(data1,data_all,side='right')/(1.0*n1)
    print(cdf1)
    cdf2 = (np.searchsorted(data2,data_all,side='right'))/(1.0*n2)
    print(cdf2)
    ks = np.max(np.absolute(cdf1-cdf2))
    cdf1_df = pd.DataFrame(cdf1)
    cdf2_df = pd.DataFrame(cdf2)
    cdf_df = pd.concat([cdf1_df,cdf2_df],axis = 1)
    cdf_df.columns = ['cdf_Bad','cdf_Good']
    cdf_df['gap'] = cdf_df['cdf_Bad']-cdf_df['cdf_Good']
    return ks,cdf_df

##test1
data_test_1 = {'y30':[1,1,1,1,1,1,0,0,0,0,0,0],'a':[1,2,4,2,2,6,5,3,0,5,4,18]}
data_test_1 = pd.DataFrame(data_test_1)
ks_2samp,cdf_2samp = ks_calc_2samp(data_test_1, ['a'], ['y30'])
#ks_2samp
#cdf_2samp


def ks_calc_cross(data,score_col,class_col):
    '''
    功能: 计算KS值，输出对应分割点和累计分布函数曲线图
    输入值:
    data: 二维数组或dataframe，包括模型得分和真实的标签
    score_col: 一维数组或series，代表模型得分（一般为预测正类的概率）
    class_col: 一维数组或series，代表真实的标签（{0,1}或{-1,1}）
    输出值:
    'ks': KS值，'crossdens': 好坏人累积概率分布以及其差值gap
    '''
    ks_dict = {}
    crossfreq = pd.crosstab(data[score_col[0]],data[class_col[0]])
    crossdens = crossfreq.cumsum(axis=0) / crossfreq.sum()
    crossdens['gap'] = abs(crossdens[0] - crossdens[1])
    ks = crossdens[crossdens['gap'] == crossdens['gap'].max()]
    return ks,crossdens

##test3
data_test_2 = {'y30':[1,1,1,1,1,1,0,0,0,0,0,0,0],'a':[1,2,0,2,2,7,4,5,4,0,4,18,np.nan]}
data_test_2 = pd.DataFrame(data_test_2)
ks_cross,cdf_cross = ks_calc_cross(data_test_2, ['a'], ['y30'])
ks_cross
cdf_cross


from sklearn.metrics import roc_curve,auc
def ks_calc_auc(data,score_col,class_col):
    '''
    功能: 计算KS值，输出对应分割点和累计分布函数曲线图
    输入值:
    data: 二维数组或dataframe，包括模型得分和真实的标签
    score_col: 一维数组或series，代表模型得分（一般为预测正类的概率）
    class_col: 一维数组或series，代表真实的标签（{0,1}或{-1,1}）
    输出值:
    'ks': KS值
    '''
    fpr,tpr,threshold = roc_curve((1-data[class_col[0]]).ravel(),data[score_col[0]].ravel())
    ks = max(tpr-fpr)
    return ks



##test
data_test_2 = {'y30':[1,1,1,1,1,1,0,0,0,0,0,0,0],'a':[1,2,0,2,2,7,4,5,4,0,4,18,np.nan]}
data_test_2 = pd.DataFrame(data_test_2)
ks_2samp,cdf_2samp = ks_calc_2samp(data_test_2, ['a'], ['y30'])
ks_2samp
cdf_2samp



##test4
ks_auc = ks_calc_auc(data_test_2, ['a'], ['y30'])
ks_auc




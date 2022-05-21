# -*- coding: utf-8 -*-
"""

@author: jamie
"""

import os
import numpy as np
import pandas as pd
import shutil

result=[]
dirs = 'H:/usgs_splib07/ASCIIdata/ASCIIdata_splib07b/Minerals'#原始文件所在。
dirs_list = os.listdir(dirs)
# print('原有文件个数',(dirs_list.__len__()))
# print('result',(result.__len__()))
D=r'H:\usgs_splib07\ASCIIdata\ASCIIdata_splib07b\M3a'#新文件夹名称（先建好）
def search(path=".", name=""):
    for item in os.listdir(path):#读取路径内的所有文件
        # print('item',item) 
        item_path = os.path.join(path, item)#连接两个或更多的路径名组件
        # print('item_path',item_path)
        if os.path.isdir(item_path):
            search(item_path, name)
        elif os.path.isfile(item_path):
            if name in item:
                global result
                # result.append(item_path + ";")#yuan 
                result.append(item_path) 
                
search(path=dirs , name="BECKa")
np.savetxt(r"H:\usgs_splib07\ASCIIdata\ASCIIdata_splib07b\M3a.txt",result,fmt='%s')
'''改好再使用'''
for item in result:
    # print(item)
    shutil.copy(item, D)
    # shutil.copy(item, newdirs)



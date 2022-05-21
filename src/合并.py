# -*- coding: utf-8 -*-
"""
Created on Tue Dec 22 19:56:29 2020

@author: asus
"""
import pandas as pd
import os
import xlsxwriter   #导入模块

 
pwd = 'C:/Users/asus/Desktop/data' # 获取文件目录
 
# 新建列表，存放文件名
file_list = []
 
# 新建列表存放每个文件数据(依次读取多个相同结构的Excel文件并创建DataFrame)
dfs = []
 
for root,dirs,files in os.walk(pwd): # 第一个为起始路径，第二个为起始路径下的文件夹，第三个是起始路径下的文件。
  for file in files:
    file_path = os.path.join(root, file)
    file_list.append(file_path) # 使用os.path.join(dirpath, name)得到全路径
    df = pd.read_excel(file_path) # 将excel转换成DataFrame
    dfs.append(df)
 
# 将多个DataFrame合并为一个
df = pd.concat(dfs,axis=1)
 
# 写入excel文件，不包含索引数据
df.to_excel('C:/Users/asus/Desktop/19W/he/result1.xlsx',index=False,float_format=True)

# workbook = xlsxwriter.Workbook('C:/Users/asus/Desktop/19W/he/result1.xlsx')     #新建excel表
# worksheet = workbook.add_worksheet('sheet1')       #新建sheet（sheet的名称为"sheet1"）
# worksheet.write(df)

# workbook.close()

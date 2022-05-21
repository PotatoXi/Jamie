# -*- coding: utf-8 -*-
"""
@author: jamie
Progress is the activity of today and the assurance of tomorrow ！

"""
import numpy as np
import random
from collections import Counter
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator


#光谱图
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import fmin,fminbound
from scipy.interpolate import make_interp_spline
import math
import os

#数据
re = open('H:/桌面/1.txt')#归一化数据
r = Counter(re)
print('统计：',r)

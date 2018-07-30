# -*- coding: utf-8 -*-
"""
Created on Tue Jul 24 20:10:27 2018

@author: Administrator
"""

import time
from lagou import lgjob

while True:
    print(lgjob.find().count())
    time.sleep(5)

# import time
# from lagou import lagoujob
#
# while True:
#     print(lagoujob.find().count())
#     time.sleep(5)
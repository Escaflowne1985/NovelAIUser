# env nsfw_predict.py/py
# -*- coding: UTF-8 -*-
'''
@Project ：nsfw_predict.py 
@File    ：test.py
@IDE     ：PyCharm 
@Author  ：Mr数据杨
@Date    ：2023/5/6 16:11 
'''

from nsfw_detector import predict
model = predict.load_model('./nsfw_mobilenet2.224x224.h5')

print(predict.classify(model, 'a.png'))
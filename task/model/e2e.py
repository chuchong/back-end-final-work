#coding=utf-8
from keras import backend as K
from keras.models import load_model
from keras.layers import *
import numpy as np
import random
import string
import matplotlib.pyplot  as plt
import keras
import cv2
from . import e2emodel as model
from . import grumodel as grum
import time
import os
from back_end import settings
import tensorflow as tf
chars = ["京", "沪", "津", "渝", "冀", "晋", "蒙", "辽", "吉", "黑", "苏", "浙", "皖", "闽", "赣", "鲁", "豫", "鄂", "湘", "粤", "桂",
             "琼", "川", "贵", "云", "藏", "陕", "甘", "青", "宁", "新", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "A",
             "B", "C", "D", "E", "F", "G", "H", "J", "K", "L", "M", "N", "P", "Q", "R", "S", "T", "U", "V", "W", "X",
             "Y", "Z","港","学","使","警","澳","挂","军","北","南","广","沈","兰","成","济","海","民","航","空"
             ]



class e2e:
    rnn = model.construct_model(os.path.join(settings.MODEL_DIR, "ocr_plate_all_w_rnn_2.h5"))
    graph_1 = tf.get_default_graph()
    gru = grum.construct_model(os.path.join(settings.MODEL_DIR, "ocr_plate_all_gru.h5"))
    graph_2 = tf.get_default_graph()
    rnn.predict(np.zeros((1,160,40,3)))
    gru.predict(np.zeros((1,164,48,3)))

    def __init__(self, type):
        '''
        :param type: 0 RNN; 1 GRU
        '''
        self.type = type
        if type == 0:
            self.pred_model = e2e.rnn
            self.graph = e2e.graph_1
            self.width, self.height = 160, 40
        else:

            self.pred_model = e2e.gru
            self.graph = e2e.graph_2
            self.width, self.height = 164, 48



    def fastdecode(self, y_pred):
        results = ""
        confidence = 0.0
        table_pred = y_pred.reshape(-1, len(chars)+1)

        res = table_pred.argmax(axis=1)
        # print('debug e2e res{}'.format(res))
        for i,one in enumerate(res):
            if one<len(chars) and (i==0 or (one!=res[i-1])):# 识别时会出现重复问题,而固定空格为83
                results+= chars[one]
                confidence+=table_pred[i][one]
        confidence/= len(results)
        # print('debug e2e result{}'.format(results))
        return results,confidence

    def recognizeOne(self, src):
        # pred_model.summary()

        # x_tempx= cv2.imread(src)
        x_tempx = src
        # x_tempx = cv2.bitwise_not(x_tempx)
        # x_temp = cv2.resize(x_tempx,( 160,40))
        x_temp = cv2.resize(x_tempx, (self.width, self.height))
        x_temp = x_temp.transpose(1, 0, 2)

        t0 = time.time()

        # if self.type == 0:
        #     with e2e.graph_1.as_default():
        #         y_pred = self.pred_model.predict(np.array([x_temp]))
        #         y_pred = y_pred[:, 2:, :]
        # else:
        #     with e2e.graph_2.as_default():
        #         y_pred = self.pred_model.predict(np.array([x_temp]))
        #         y_pred = y_pred[:,2:,:]
        # 1 14 1 84
        # plt.imshow(y_pred.reshape(-1,84))
        # plt.show()

        with self.graph.as_default():
            y_pred = self.pred_model.predict(np.array([x_temp]))
            y_pred = y_pred[:, 2:, :]

        #
        # cv2.imshow("x_temp",x_tempx)
        # cv2.waitKey(0)
        return self.fastdecode(y_pred)
    #
    #
    # import os
    #
    # path = "/Users/yujinke/PycharmProjects/HyperLPR_Python_web/cache/finemapping"
    # for filename in os.listdir(path):
    #     if filename.endswith(".png") or filename.endswith(".jpg") or filename.endswith(".bmp"):
    #         x = os.path.join(path,filename)
    #         recognizeOne(x)
    #         # print time.time() - t0
    #
    #         # cv2.imshow("x",x)
    #         # cv2.waitKey()

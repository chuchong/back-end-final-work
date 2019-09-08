# print(__name__)
# __name__ = 'model'
import cv2
import numpy as np
from task.model import pipline as pp
import json
# image = cv2.imread("demo1.png", cv2.CV_8UC1)
#识别结果 单个文字
# print(hyperlpr_py3.recognizer.SimplePredict(image,0))
# print(hyperlpr_py3.recognizer.SimplePredict(image,1))
# print(hyperlpr_py3.recognizer.SimplePredict(image,2))
from back_end import settings
import os
def CNNTest(file):
    image = cv2.imread(os.path.join(settings.MEDIA_ROOT, file))
    # print( type(image))
    res = json.loads(pp.RecognizePlateJson(image, 1))
    res = pp.SimpleRecognizePlateByE2E(image,0)

    # for jre in res:
    #     x,y,w,h = jre['x'],jre['y'],jre['w'],jre['h']
    #     print([x,y,w,h])

def GRUTest(file):
    pass

# main()
def twice_test(file):
    CNNTest(file)
    GRUTest(file)

def main():
    a = np.array([255])
    b = a.astype(np.uint8)
    twice_test('2.jpg')



main()
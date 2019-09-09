import cv2
from . import model
import task.model.pipline as pp
import numpy as np
import re

def cv_imread(filePath):
    cv_img=cv2.imdecode(np.fromfile(filePath,dtype=np.uint8),-1)
    ## imdecode读取的是rgb，如果后续需要opencv处理的话，需要转换成bgr，转换后图片颜色会变化
    ##cv_img=cv2.cvtColor(cv_img,cv2.COLOR_RGB2BGR)
    return cv_img

def vary_handle(image, type):

    # assert (image is not None)
    image, res = pp.SimpleRecognizePlateByE2E(image, 0)

    return image, res



def handle(image_url):

    # raise Exception(image_url)
    image = cv_imread(image_url)
    reg = re.compile('\..*?$')
    suffixs = reg.findall(image_url)
    for su in suffixs:
       suf = su

    assert (image is not None)
    image1,res1 = vary_handle(image, 0)

    cv2.imencode(suf, image1)[1].tofile(image_url+'__1.jpg')
    # cv2.imwrite(image_url+'__1.jpg', image1)

    assert (image is not None)
    image2,res2 = vary_handle(image, 1)

    cv2.imencode(suf , image2)[1].tofile(image_url+'__2.jpg')
    # cv2.imwrite(image_url+'__2.jpg', image2)
    return res1,res2
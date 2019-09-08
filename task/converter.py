import cv2
from . import model
import task.model.pipline as pp

def handle(image_url):
    image = cv2.imread(image_url)
    image_set = []
    res_set = []
    for tpe in range(2):
        image, res = pp.SimpleRecognizePlateByE2E(image, tpe)
        image_set.append(image)
        res_set.append(res)
    cv2.imwrite(image_url+'__1.jpg', image_set[0])
    cv2.imwrite(image_url+'__2.jpg', image_set[1])
    return image_set , res_set
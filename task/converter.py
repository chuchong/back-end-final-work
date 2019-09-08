import cv2
from . import model
import task.model.pipline as pp

def vary_handle(image, type):
    image, res = pp.SimpleRecognizePlateByE2E(image, 0)

    return image, res



def handle(image_url):
    image = cv2.imread(image_url)
    image1,res1 = vary_handle(image, 0)
    cv2.imwrite(image_url+'__1.jpg', image1)
    image2,res2 = vary_handle(image, 1)
    cv2.imwrite(image_url+'__2.jpg', image2)
    return res1,res2
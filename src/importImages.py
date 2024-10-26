import cv2
import os
import random
import numpy as np


def rotateImage(image):
    angle = -40 + random.random() * 80
    rotationMatrix = cv2.getRotationMatrix2D((320, 240), angle, 0.8)
    return cv2.warpAffine(image, rotationMatrix, (640, 480)) #640, 480



def moveImage(img):
    shiftX =  -10 + random.random() * 20
    shiftY = 0  

    move_matrix = np.float32([[1, 0, shiftX], [0, 1, shiftY]])
    dimensions = (img.shape[1], img.shape[0])
    return cv2.warpAffine(img, move_matrix, dimensions)


def zoom(img):
    border = 30 + int(random.random() * 20)
    height, width, channel = img.shape
    img = img[border:height-border, border:width-border]
    return img



def dataAugmentation(folder, categorie):
    cpt = 0

    for filename in os.listdir(folder + categorie):

        image = cv2.imread(folder + categorie + filename)
        cv2.imwrite("../augmentedBig/" + categorie + str(cpt) + ".png", image)
        cpt += 1

        for i in range(10):
            image = cv2.imread(folder + categorie + filename)
        
            image = rotateImage(image)
            image = moveImage(image)
            image = zoom(image)
            image = cv2.resize(image, (640, 480))
        
            cv2.imwrite("../augmentedBig/" + categorie + str(cpt) + ".png", image)
            cpt += 1



dataAugmentation("../dataset/", "Defaut/inf/")
dataAugmentation("../dataset/", "Sans_Defaut/")




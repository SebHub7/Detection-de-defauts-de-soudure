import pygame
import os
import cv2

class ImageZone:

    def __init__(self, imageName, predictionURL, x, y, w, h, text):
        self.imageName = imageName
        self.predictionURL = predictionURL
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.font = pygame.font.SysFont('Corbel', 20, bold=True) 
        self.text = self.font.render(text, True, (0, 0, 0))



    def drawImages(self, window, currentImageURL):
    
        if currentImageURL != None:

            if os.path.isdir("runs") and os.path.isfile("runs/detect/" + self.predictionURL + self.imageName):
                img = pygame.image.load("runs/detect/" + self.predictionURL + self.imageName)
                img = pygame.transform.scale(img, (self.w, self.h))
                window.blit(img, (self.x, self.y))

        window.blit(self.text, (self.x, self.y+self.h)) 




    def drawStat(self, window, imageURL):
        img = cv2.imread(imageURL)
        img = cv2.resize(img, (self.w, self.h))
        img = pygame.image.frombuffer(img.tostring(), img.shape[1::-1], "BGR")
        window.blit(img, (self.x, self.y))
        window.blit(self.text, (self.x, self.y+self.h)) 

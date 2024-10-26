import pygame
from pygame_widgets.slider import Slider
from pygame.locals import QUIT
from button import *
from tkinter import filedialog
from tkinter import *
import os
from model import *
from ImageZone import *


class Menu:
    def __init__(self, width, height):
        self.w = width
        self.h = height
        self.currentImageURL = None
        self.currentImageName = None
        self.displayedImage = [1, 1, 1, 0, 0, 0]

        self.btn_clicked = "image"

        # UI
        pygame.init()
        self.font = pygame.font.SysFont('Corbel', 20, bold=True) 

        pygame.display.set_caption('Projet Soudures Infrarouges')
        self.window = pygame.display.set_mode((width, height))
        self.select_btn = Button1(20, 10, 100, 30, "Select a file")
        self.show_precision_btn = Button1(140, 10, 130, 30, "Show precision")
        self.show_confusion_btn = Button1(290, 10, 140, 30, "Show confusion")
        self.show_loss_btn = Button1(445, 10, 95, 30, "Show loss")
        self.conf_threshold = Button1(920, 10, 200, 40, "Seuil de confiance: 0.00")

        self.next_page_btn = Button1(120, 650, 50, 30, "Next")
        self.previous_page_btn = Button1(20, 650, 80, 30, "Previous")

        self.slider = Slider(self.window, 700, 10, 200, 20, min=0, max=99, step=1, initial=0)
        self.oldSliderValue = 0

        # Instanciate image Zones
        self.imagesZone = []
        predictionsURL = ["predict4/", "predict5/", "predict6/", "predict/", "predict2/", "predict3/"]
        names = ["YOLO random 1056 images", "YOLO pretrained 1056 images", "YOLO transfer learning 1056 images",
                 "YOLO random 189 images", "YOLO pretrained 189 images", "YOLO transfer learning 189 images"]

        for y in range(2):
            for x in range(3):
                self.imagesZone.append(ImageZone("", predictionsURL[y*3 + x], 20 + x*510, 80, 500, 500, names[y*3 + x]))

        # creating a model containing all yolo models
        self.model = Model()



    def drawImages(self):
        
        if self.currentImageURL != None:
            #img = pygame.image.load(self.currentImageURL)
            #img = pygame.transform.scale(img, (210, 210))
            #self.window.blit(img, (20, 380))

            for i in range(len(self.imagesZone)):
                
                if self.displayedImage[i] == 1:
                    self.imagesZone[i].imageName = self.currentImageName
                    self.imagesZone[i].drawImages(self.window, self.currentImageURL)



    def drawStats(self):

        links = ["../yolo_model/v4/yolov8_random/",
                 "../yolo_model/v4/yolov8_pretrained/",
                 "../yolo_model/v4/yolov8_transfer_learning/",
                 "../yolo_model/v2/yolov8_random/",
                 "../yolo_model/v2/yolov8_pretrained/",
                 "../yolo_model/v2/yolov8_transfer_learning/"
                 ]
        

        for i in range(len(self.imagesZone)):

            if self.displayedImage[i] == 1:
                if self.btn_clicked == "precision":
                    self.imagesZone[i].drawStat(self.window, links[i] + "P_curve.png")

                elif self.btn_clicked == "confusion":
                    self.imagesZone[i].drawStat(self.window, links[i] + "confusion_matrix.png")

                elif self.btn_clicked == "loss":
                    self.imagesZone[i].drawStat(self.window, links[i] + "loss.png")
            




    def display(self):
        self.window.fill((220, 220, 220)) 
        self.select_btn.draw(self.window)
        self.show_precision_btn.draw(self.window)
        self.show_confusion_btn.draw(self.window)
        self.show_loss_btn.draw(self.window)
        self.next_page_btn.draw(self.window)
        self.previous_page_btn.draw(self.window)


        #if self.currentImageURL != None:
           #self.conf_threshold.draw(self.window)

        if self.btn_clicked == "image":
            self.drawImages()

        else:
            self.drawStats()



    def eventButton(self):
        if self.select_btn.isClicked():
            self.btn_clicked = "image"

            root = Tk()
            root.withdraw()
            self.currentImageURL = filedialog.askopenfilename()
            split = os.path.split(self.currentImageURL)
            self.currentImageName = split[1]
            self.model.predictAll(self.currentImageURL, self.slider.getValue())


        elif self.show_precision_btn.isClicked():
            self.btn_clicked = "precision"

        elif self.show_confusion_btn.isClicked():
            self.btn_clicked = "confusion"

        elif self.show_loss_btn.isClicked():
            self.btn_clicked = "loss"

        elif self.next_page_btn.isClicked():
            self.displayedImage = [0, 0, 0, 1, 1, 1]
        
        elif self.previous_page_btn.isClicked():
            self.displayedImage = [1, 1, 1, 0, 0, 0]

        self.display()







    def runWindow(self):
        
        self.display()

        run = True
        while run:

            events = pygame.event.get()

            for event in events:
                if event.type == QUIT:
                    run = False

                if event.type == pygame.MOUSEBUTTONDOWN: 
                    self.eventButton()


                if event.type == pygame.MOUSEBUTTONUP: 
                    if self.currentImageURL != None:
                        if self.slider.getValue() != self.oldSliderValue:

                            self.oldSliderValue = self.slider.getValue()
                            self.model.predictAll(self.currentImageURL, self.slider.getValue())
                            self.conf_threshold.text =  self.conf_threshold.font.render("Seuil de confiance: " + str(self.slider.getValue() / 100), True, (0, 0, 0))
                            self.display()

                        #pygame_widgets.update(events)
            pygame.display.update() 
            pygame.time.delay(50)

        pygame.quit()

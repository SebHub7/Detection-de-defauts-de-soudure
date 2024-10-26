import os
import shutil
from ultralytics import YOLO


class Model:

    def __init__(self):
        self.models = []

        self.models.append(YOLO('../yolo_model/v2/yolov8_random/best.pt'))
        self.models.append(YOLO('../yolo_model/v2/yolov8_pretrained/best.pt'))
        self.models.append(YOLO('../yolo_model/v2/yolov8_transfer_learning/best.pt'))

        self.models.append(YOLO('../yolo_model/v4/yolov8_random/best.pt'))
        self.models.append(YOLO('../yolo_model/v4/yolov8_pretrained/best.pt'))
        self.models.append(YOLO('../yolo_model/v4/yolov8_transfer_learning/best.pt'))
 

    def predictModel(self, model, currentImageURL, sliderValue):

        res = model.predict(currentImageURL, save=False, imgsz=320, conf=sliderValue/100, max_det=2)
        classes = res[0].names
        predicted_classes = res[0].boxes.cls

        # len tested to avoid no prediction reading
        if len(predicted_classes) == 0:
            model.predict(currentImageURL, save=True, imgsz=320, conf=sliderValue/100, max_det=1)

        elif len(predicted_classes) == 1:
            model.predict(currentImageURL, save=True, imgsz=320, conf=sliderValue/100, max_det=1)

        elif len(predicted_classes) == 2:
            first_prediction = str(classes[predicted_classes[0].item()])
            second_prediction = str(classes[predicted_classes[1].item()])

            if first_prediction == 'sans_defaut':
                model.predict(currentImageURL, save=True, imgsz=320, conf=sliderValue/100, max_det=1)

            elif(first_prediction == second_prediction):
                model.predict(currentImageURL, save=True, imgsz=320, conf=sliderValue/100, max_det=1)

            elif(first_prediction != second_prediction):

                if second_prediction == 'sans_defaut':
                    model.predict(currentImageURL, save=True, imgsz=320, conf=sliderValue/100, max_det=1)
                else:
                    model.predict(currentImageURL, save=True, imgsz=320, conf=sliderValue/100, max_det=2)


    def predictAll(self, currentImageURL, sliderValue):
        if os.path.isdir("runs"):
            shutil.rmtree("runs")

        for i in range(len(self.models)):        
            self.predictModel(self.models[i], currentImageURL, sliderValue)


    def getValidationStats(self):
        result = []
        result.append(self.model1.val(data='data/data.yaml', save_json=True))
        result.append(self.model2.val(data='data/data.yaml', save_json=True))
        result.append(self.model3.val(data='data/data.yaml', save_json=True))

        return result
    


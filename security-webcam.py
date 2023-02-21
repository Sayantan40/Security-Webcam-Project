## Importing the necessary libraries abd modules
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUiType
import sys
import cv2
import winsound

ui,_=loadUiType(r'C:\Users\sayan\Webcam Security Camera Project\templates\pyqt-security-webcam.ui')

class  App(QMainWindow,ui):
    
    volume = 500
    
    def __init__(self):
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.MONITORING.clicked.connect(self.start_monitoring)
        self.VOLUME.clicked.connect(self.set_volume)
        self.EXIT.clicked.connect(self.close_window) 
        self.VOLUMESLIDER.setVisible(False)
        self.VOLUMESLIDER.valueChanged.connect(self.set_volume_level)

    
    ## This function is to start monitoring of the webcam
    def start_monitoring(self):
        print("Start monitoring button clicked")
        ## This object is to start the wwebcam and 0 indicates that we have only one webcam.
        webcam = cv2.VideoCapture(0)
        while True:
            _,im1 = webcam.read()
            _,im2 = webcam.read()
            # Here we compare the difference between the im1 image and the im2 image.
            diff = cv2.absdiff(im1,im2)
            ## this will convert  diff image into gray scale image
            gray = cv2.cvtColor(diff,cv2.COLOR_BGR2GRAY)
            ## this will blur the diff gray scale image
            blur = cv2.GaussianBlur(gray,(5,5),0)
            ## This will make the threshold image
            _,thresh = cv2.threshold(blur, 20,255,cv2.THRESH_BINARY)
            dilated = cv2.dilate(thresh,None,iterations=3)
            countours,_=cv2.findContours(dilated,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
            for i in countours:
                if cv2.contourArea(i) <8000:
                    continue
                ## THe  boundary position of the rectangle
                x,y,w,h = cv2.boundingRect(i)
                cv2.rectangle(im1,(x,y),(x+w,y+h),(0,255,0),2)
                cv2.imwrite('captured.jpg',im1)
                image = QImage('captured.jpg')
                ## Object of the captured image
                pm = QPixmap.fromImage(image)
                ## Display the captured image in the app screen
                self.CAMWINDOW.setPixmap(pm)
                winsound.Beep(self.volume,100)
            cv2.imshow("Opencv-Security-Camera",im1)
            
            key = cv2.waitKey(10)
            if key == 27:
                break
        webcam.release() 
        ## THis will close the application window once it has capturedthe necessary image
        cv2.destroyAllWindows()  
    
    
    ## This function is set the volume of the alarm.
    def set_volume(self):
        self.VOLUMESLIDER.setVisible(True)
        print("Set volume button clicked")

    
    ## This function is to close the application window
    def close_window(self):
        self.close()
    
    
    ## This function is set the level of the volume of the alarm
    def set_volume_level(self):
        self.VOLUMELEVEL.setText(str(self.VOLUMESLIDER.value()//10))
        self.volume = self.VOLUMESLIDER.value() * 10
        ## THe 1000 here means 1000 milliseconds that is 1 second
        cv2.waitKey(1000)  
        self.VOLUMESLIDER.setVisible(False)


    
def main():
    app = QApplication(sys.argv)
    window = App()
    window.show()
    app.exec_()
if __name__ == '__main__':
    main()  

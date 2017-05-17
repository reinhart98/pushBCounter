#!/usr/bin/python3
# -*- coding: utf-8 -*-


import RPi.GPIO as GPIO
import time

import sys
from PyQt5.QtWidgets import QMainWindow, QPushButton, QApplication
GPIO.setmode(GPIO.BOARD)

from PyQt5 import QtCore

counter = 0

class Example(QMainWindow):

    def __init__(self):
        super().__init__()
        self.initUI()
        self.tactile = TactileListener(self)
        self.tactile.start()
        self.tactile.valueUpdated.connect(self.updateCounter)
         
    def updateCounter(self, value):
        self.btn1.setText(str(value))
        if value % 2 == 0:
            self.btn1.setStyleSheet("background-color:blue")
        else:
            self.btn1.setStyleSheet("background-color:yellow")
    def initUI(self):      

        self.btn1 = QPushButton("Counter", self)
        self.btn1.move(30, 50)
        self.btn1.setStyleSheet("background-color:black")
 
        self.statusBar()
        
        self.setGeometry(500, 300, 150, 150)
        self.setWindowTitle('Toggle Warna')
        self.show()

class TactileListener(QtCore.QThread):
    valueUpdated = QtCore.pyqtSignal(int)
    def run(self):
        counter = 0
        switch_pin = 40
        led_pin=12
        GPIO.setup(switch_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(led_pin, GPIO.OUT)
        button_state=False
        led_state=False
        old_input_state = True
        while True:
            new_input_state = GPIO.input(switch_pin)
            if new_input_state == False and old_input_state == True:
                button_state = not button_state
                led_state = not led_state
                counter+=1
                
                self.valueUpdated.emit(counter)      
            old_input_state = new_input_state
            GPIO.output(led_pin, led_state)
                                
            time.sleep(0.05)




if __name__ == '__main__':
    
 
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())

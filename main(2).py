from PyQt5 import QtCore, QtGui, QtWidgets
from gui2 import Ui_MainWindow
import cv2 as cv
import numpy as np
import sys
import os
from modes import modes
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QLabel, QFileDialog, QAction , QComboBox ,QMessageBox
from PyQt5.QtGui import QIcon, QPixmap ,QImage
import pyqtgraph as pg
from pyqtgraph import ImageView
import logging
logging.basicConfig(level=logging.DEBUG,
                    filename="follow.log",
                    format='%(lineno)s - %(levelname)s - %(message)s',
                    filemode='w')
logger = logging.getLogger()
class mainwindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(mainwindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.plot = [self.ui.image1, self.ui.image2, self.ui.updated1, self.ui.updated2, self.ui.output1,
                     self.ui.output2]
        for i in range(len(self.plot)):
            self.plot[i].ui.histogram.hide()
            self.plot[i].ui.roiBtn.hide()
            self.plot[i].ui.menuBtn.hide()
            self.plot[i].ui.roiPlot.hide()

        self.comboboxes = [self.ui.comboBox1 , self.ui.comboBox2 ,self.ui.comboBox5,self.ui.comboBox7 ,
                           self.ui.comboBox3 ,self.ui.comboBox4,self.ui.comboBox6 ]

        self.component = ['Mag,phase,Real,imag', 'magnitude', 'phase', 'real', 'imaginary']
        self.ui.comboBox1.addItems(self.component)
        self.ui.comboBox2.addItems(self.component)
        self.mix = ['mode', 'magnitude', 'phase', 'real', 'imaginary', 'uniform magnitude', 'uniform phase']
        self.ui.comboBox5.addItems(self.mix)
        self.ui.comboBox7.addItems(self.mix)
        self.outputno = ['output', 'output 1', 'output 2']
        self.ui.comboBox3.addItems(self.outputno)
        self.imageno = ['image1,2', 'image 1', 'image 2']
        self.ui.comboBox4.addItems(self.imageno)
        self.ui.comboBox6.addItems(self.imageno)

        self.gains = [self.ui.slider1, self.ui.slider2]

        self.ui.actionimage1.triggered.connect(lambda: self.open(1))
        self.ui.actionimage1.setShortcut("Ctrl+o")
        self.ui.actionimage2.triggered.connect(lambda: self.open(2))
        self.ui.actionimage2.setShortcut("Ctrl+p")
        self.comboboxes[0].currentIndexChanged.connect(lambda: self.components(0, 2,1, self.comboboxes[0].currentText()))
        self.comboboxes[1].currentIndexChanged.connect(lambda: self.components(1, 3,2, self.comboboxes[1].currentText()))
        self.comboboxes[4].currentIndexChanged.connect(lambda: self.outputplace())
        self.comboboxes[5].currentIndexChanged.connect(lambda: self.source())
        self.comboboxes[6].currentIndexChanged.connect(lambda: self.source())
        self.comboboxes[2].currentIndexChanged.connect(lambda: self.othercomponent(2, 3))
        # self.comboboxes[3].currentIndexChanged.connect(lambda: self.othercomponent(3, 2))
        self.Mixer_options = [["magnitude", "uniform magnitude"], ["phase", "uniform phase"], ["real"], ["imaginary"]]
        # self.mix = ['mode', 'magnitude', 'phase', 'real', 'imaginary', 'uniform magnitude', 'uniform phase']
        self.gains[0].sliderReleased.connect(lambda: self.drawmix())
        self.gains[1].sliderReleased.connect(lambda: self.drawmix())
    def open(self, number) :
        filename = QFileDialog.getOpenFileName(self)
        if filename[0]:
            self.path = filename[0]
            self.read(self.path, number)
    def read(self, path, number):
        if number == 1 :
            self.img1 = modes(path)
            self.plot[0].show()
            self.plot[0].setImage(self.img1.img.T)
            self.images = [self.img1]
            logger.info('User start to choose image 1')
        elif number == 2 :
            self.img2 = modes(path)
            logger.info('User start to choose image 2')
            if self.img2.img.shape != self.img1.img.shape:
                error_message = QMessageBox()
                error_message.setIcon(QMessageBox.Question)
                error_message.setText("Please, Enter Image2 with the same size of image1" )
                error_message.setWindowTitle("Error")
                error_message.exec_()
                logger.warning("user enter image of wrong size")
            else:
                self.img2 = modes(path)
                self.plot[1].show()
                self.plot[1].setImage(self.img2.img.T)
                self.images = [self.img1,self.img2]
    def components(self, imageOriginalNum, imageBoxNum,imgno, mode):
        self.plot[imageBoxNum].show()
        if mode == self.component[1]:
            self.plot[imageBoxNum].setImage((self.images[imageOriginalNum].mag.T))
        elif mode == self.component[2]:
            self.plot[imageBoxNum].setImage(self.images[imageOriginalNum].phase.T)
        elif mode == self.component[3]:
            self.plot[imageBoxNum].setImage((self.images[imageOriginalNum].real.T))
        elif mode == self.component[4]:
            self.plot[imageBoxNum].setImage(self.images[imageOriginalNum].imaginary.T)
        logger.info(f"plot {mode}  of image {imgno} ")

    def outputplace(self):
        if self.comboboxes[4].currentText() == 'output 1' :
            self.mixplace = self.plot[4]
        elif self.comboboxes[4].currentText() == 'output 2' :
            self.mixplace = self.plot[5]
    def source(self):
        if self.comboboxes[5].currentText() == 'image 1' :
            self.source1 = self.img1
        elif self.comboboxes[5].currentText() == 'image 2' :
            self.source1 = self.img2
        if self.comboboxes[6].currentText() == 'image 1' :
            self.source2 = self.img1
        elif self.comboboxes[6].currentText() == 'image 2' :
            self.source2 = self.img2
    def othercomponent(self ,mode1 ,mode2 ):
        self.comboboxes[mode2].clear()
        for Mixer_option in range(len(self.Mixer_options)):
            if self.comboboxes[mode1].currentText().lower() in self.Mixer_options[Mixer_option]:
                if Mixer_option % 2 == 0:
                    Mixer_option = Mixer_option + 1
                else:
                    Mixer_option = Mixer_option - 1
                self.comboboxes[mode2].addItems(self.Mixer_options[Mixer_option])

    def drawmix(self):
        data = ...
        firstvalue = self.gains[0].value() / 100
        secondvalue = self.gains[1].value() / 100
        self.comp1=self.comboboxes[2].currentText()
        self.comp2=self.comboboxes[3].currentText()
        if (self.comboboxes[2].currentText() == 'magnitude' and self.comboboxes[3].currentText() == 'phase') or(self.comboboxes[2].currentText() == 'real' and self.comboboxes[3].currentText() == 'imaginary') or (self.comboboxes[2].currentText() == 'magnitude' and self.comboboxes[3].currentText() == 'uniform phase') or (self.comboboxes[2].currentText() == 'uniform magnitude' and self.comboboxes[3].currentText() == 'phase') or (self.comboboxes[2].currentText() == 'uniform magnitude' and self.comboboxes[3].currentText() == 'uniform phase'):
            data = self.source1.mix(self.source2, firstvalue, secondvalue, self.comp1 , self.comp2 )
        elif (self.comboboxes[2].currentText() == 'phase' and self.comboboxes[3].currentText() == 'magnitude') or (self.comboboxes[2].currentText() == 'imaginary' and self.comboboxes[3].currentText() == 'real') or (self.comboboxes[2].currentText() == 'uniform phase' and self.comboboxes[3].currentText() == 'magnitude') or (self.comboboxes[2].currentText() == 'phase' and self.comboboxes[3].currentText() == 'uniform magnitude') or (self.comboboxes[2].currentText() == 'uniform phase' and self.comboboxes[3].currentText() == 'uniform magnitude'):
            data = self.source2.mix(self.source1, secondvalue, firstvalue, self.comp1 , self.comp2 )
        self.mixplace.show()
        self.mixplace.setImage(data.T)
        if type(data) != type(...):
            logger.info(
                f"Mixing {firstvalue} {self.comboboxes[2].currentText()} From {self.comboboxes[5].currentText() } And {secondvalue}"
                f" {self.comboboxes[3].currentText()} From {self.comboboxes[6].currentText()}")
            logger.info(f"{self.comboboxes[4].currentText()} has been generated and displayed")

def main():
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    app = QtWidgets.QApplication(sys.argv)
    application = mainwindow()
    application.show()
    app.exec_()


if __name__ == "__main__":
    main()



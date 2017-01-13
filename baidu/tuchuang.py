# -*- coding=utf8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
from PyQt4 import QtCore, QtGui, uic
import requests
import re
from smms import smms

qtCreatorFile = "tuchuang_ui.ui" # Enter file here.

Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)

class MyApp(QtGui.QMainWindow, Ui_MainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        self.thread=Worker()
        self.fileSelect.clicked.connect(self.selectFile)
        self.thread.sinOut2.connect(self.show_result)

    def selectFile(self):
        filepath=self.to_utf8(QtGui.QFileDialog.getOpenFileName(self,u'选择图片','',r'Image Files(*.png *.jpg *.bmp *.jpeg *.gif)'))
        self.thread.getPath((filepath,))
        self.fileSelect.setEnabled(False)


    def show_result(self,result):
        img,isTrue=result[0],result[1]
        self.markdown_show.setText('![]('+img+')')
        self.realurl.setText(img)
        self.fileSelect.setEnabled(isTrue)

    def to_utf8(self,input):
        return unicode(input,'utf8','ignore')


class Worker(QtCore.QThread): 
    sinOut2 = QtCore.pyqtSignal(tuple) 

    def __init__(self,parent=None): 
        super(Worker,self).__init__(parent) 

    def getPath(self,filepath):
        self.filepath=filepath[0]
        self.start()
        

    def run(self):
        img=smms(self.filepath)
        self.sinOut2.emit((img,True))


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())

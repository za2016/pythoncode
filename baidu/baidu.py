# -*- coding=utf8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
from PyQt4 import QtCore, QtGui, uic
import requests
import re

tc_api='http://image.baidu.com/pictureup/uploadshitu'
files={
    'image':''
    }
data={'pos':'upload'
    ,'uptype':'upload_pc'
    ,'fm':'index'}

def upload_file(filepath):
    try:
        img=open(filepath,'rb')
    except Exception,e:
        print e
        sys.exit(0)
    files['image']=img
    c=requests.post(tc_api,files=files,data=data)
    img_url=re.findall('queryImageUrl=(.*?)&querySign',c.url)[0]
    img1=re.sub('%3A',':',img_url)
    img2=re.sub('%2F','/',img1)
    return img2

qtCreatorFile = "baidu_ui.ui" # Enter file here.

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
        try:
            img=open(self.filepath,'rb')
        except Exception,e:
            print e
            sys.exit(0)
        files['image']=img
        c=requests.post(tc_api,files=files,data=data)
        img_url=re.findall('queryImageUrl=(.*?)&querySign',c.url)[0]
        img1=re.sub('%3A',':',img_url)
        img2=re.sub('%2F','/',img1)
        self.sinOut2.emit((img2,True))


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())

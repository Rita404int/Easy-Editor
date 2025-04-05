from PIL import Image
from PIL.ImageQt import ImageQt
from PIL import ImageFilter
from PIL.ImageFilter import(BLUR,SHARPEN ) 

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap 
import os
from PyQt5.QtWidgets import (
        QApplication,QWidget,QPushButton,QFileDialog,
        QHBoxLayout, QVBoxLayout,QLabel,QListWidget
)

ap = QApplication([])
main = QWidget()
main.resize(700,500)
main.setWindowTitle('Easy Editor')

Buttondir = QPushButton("Папка")
B_list = QListWidget()
Ql = QLabel("Картинка")
Buttonl = QPushButton("Лево")
Buttonr = QPushButton("Право")
Buttonm = QPushButton("Зеркало")
Buttonres = QPushButton("Резкость")
Buttongray = QPushButton("Ч/Б")

v_line1  = QVBoxLayout()
v_line2 = QVBoxLayout()
h_line1  = QHBoxLayout()
h_line2  = QHBoxLayout()


v_line1.addWidget(Buttondir)
v_line1.addWidget(B_list)
v_line2.addWidget(Ql)
h_line2.addWidget(Buttonl)
h_line2.addWidget(Buttonr)
h_line2.addWidget(Buttonm)
h_line2.addWidget(Buttonres)
h_line2.addWidget(Buttongray)
v_line2.addLayout(h_line2)
h_line1.addLayout(v_line1, 20)
h_line1.addLayout(v_line2, 80)
main.setLayout(h_line1)



workdir = ''


def filter(files, extensions):
    result = []
    for filename in files:
        for ext in extensions:
            if filename.endswith(ext):
                result.append(filename)
    return result


def chooseWorkdir():
    global workdir
    workdir = QFileDialog.getExistingDirectory()


def showFilenamesList():
    extensions = ['.jpg','.jpeg', '.png', '.gif', '.bmp']
    chooseWorkdir()
    filenames = filter(os.listdir(workdir), extensions)
    B_list.clear()
    for filename in filenames:
        B_list.addItem(filename)


Buttondir.clicked.connect(showFilenamesList)


class ImageProcessor():
    def __init__(self):
       self.image = None
       self.dir = None
       self.filename = None
       self.save_dir = "Modified/"


    def loadImage(self, filename):
       self.filename = filename
       fullname = os.path.join(workdir, filename)
       self.image = Image.open(fullname)


    def saveImage(self):
        path = os.path.join(workdir, self.save_dir)
        if not(os.path.exists(path) or os.path.isdir(path)):
            os.mkdir(path)
        fullname = os.path.join(path, self.filename)

        self.image.save(fullname)

    def do_right(self):
        self.image = self.image.transpose(Image.ROTATE_270)
        self.saveImage()
        image_path = os.path.join(workdir, self.save_dir, self.filename)
        self.showImage(image_path)


    def do_flip (self):
        self.image = self.image.transpose(Image.FLIP_LEFT_RIGHT)
        self.saveImage()
        image_path = os.path.join(workdir, self.save_dir, self.filename)
        self.showImage(image_path)


    def do_left(self):
        self.image = self.image.transpose(Image.ROTATE_90)
        self.saveImage()
        image_path = os.path.join(workdir, self.save_dir, self.filename)
        self.showImage(image_path)


    def do_blur(self):
        self.image = self.image.filter(ImageFilter.BLUR)
        self.saveImage()
        image_path = os.path.join(workdir, self.save_dir, self.filename)
        self.showImage(image_path)

    def do_black_White(self):
        self.image = self.image.convert('L')
        self.saveImage()
        image_path = os.path.join(workdir, self.save_dir, self.filename)
        self.showImage(image_path)



    def do_sharpen(self):
       self.image = self.image.filter(SHARPEN)
       self.saveImage()
       image_path = os.path.join(workdir, self.save_dir, self.filename)
       self.showImage(image_path)


    def showImage(self, path):
        Ql.hide()
        pixmapimage = QPixmap(path)
        w, h = Ql.width(), Ql.height()
        pixmapimage = pixmapimage.scaled(w, h, Qt.KeepAspectRatio)
        Ql.setPixmap(pixmapimage)
        Ql.show()


def showChosenImage():
    if B_list.currentRow() >= 0:
        filename = B_list.currentItem().text()
        workimage.loadImage(filename)
        workimage.showImage(os.path.join(workdir, workimage.filename))



workimage = ImageProcessor() 
B_list.currentRowChanged.connect(showChosenImage)


Buttongray.clicked.connect(workimage.do_black_White)
Buttonl.clicked.connect(workimage.do_left)
Buttonr.clicked.connect(workimage.do_right)
Buttonres.clicked.connect(workimage.do_sharpen)
Buttonm.clicked.connect(workimage.do_flip)


main.show()
ap.exec()








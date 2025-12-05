from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMessageBox, QWidget, QListWidget, QPushButton, QHBoxLayout, QVBoxLayout, QLabel, QFileDialog, QInputDialog
from PIL import Image
from PIL import ImageFilter
import os
from PyQt5.QtGui import QPixmap
from PIL.ImageFilter import SHARPEN

workdir = ''
app = QApplication([])
wind = QWidget()
wind.setWindowTitle('Easy Editor')
wind.resize(1150, 700)


PButton = QPushButton('Папка')
FilesList = QListWidget()
left = QPushButton('Лево')
right = QPushButton('Право')
mirror = QPushButton('Зеркало')
sharpness = QPushButton('Резкость')
B_W = QPushButton('Ч/Б')
DelButton = QPushButton('Сбросить')
lb_image = QLabel('картинка')
cropp = QPushButton('Обрезать')

vline1 = QVBoxLayout()
vline2 = QVBoxLayout()
hline1 = QHBoxLayout()
hline2 = QHBoxLayout()

vline2.addWidget(lb_image)
hline1.addWidget(left)
hline1.addWidget(right)
hline1.addWidget(mirror)
hline1.addWidget(sharpness)
hline1.addWidget(B_W)
hline1.addWidget(cropp)
hline1.addWidget(DelButton)
vline1.addWidget(PButton)
vline1.addWidget(FilesList)
vline2.addLayout(hline1)
hline2.addLayout(vline1, 20)
hline2.addLayout(vline2, 80)
wind.setLayout(hline2)

class ImageProcessor():
    def __init__(self):
        self.FName = None
        self.pic = None
        self.SubfolderName = 'subfolder/'
        self.original = None

    def loadImage(self, filename):
        self.filename = filename
        image_path = os.path.join(workdir, filename)
        self.pic = Image.open(image_path)
        self.original = self.pic.copy()

    def showImage(self, path):
        lb_image.hide()
        pixmapimage = QPixmap(path)
        w, h = lb_image.width(), lb_image.height()
        pixmapimage = pixmapimage.scaled(w, h, Qt.KeepAspectRatio)
        lb_image.setPixmap(pixmapimage)
        lb_image.show()

    def reset_image(self):
        if self.original is None:
            return
        self.pic = self.original.copy()   
        self.showImage(os.path.join(workdir, self.filename))

    def do_bw(self):
        self.pic = self.pic.convert("L")
        self.saveImage()
        image_path = os.path.join(workdir, self.SubfolderName, self.filename)
        self.showImage(image_path)

    def saveImage(self):
        path = os.path.join(workdir, self.SubfolderName)
        if not(os.path.exists(path) or os.path.isdir(path)):
            os.mkdir(path)
        image_path = os.path.join(path, self.filename)
        self.pic.save(image_path)

    def do_flip(self):
        self.pic = self.pic.transpose(Image.FLIP_LEFT_RIGHT)
        self.saveImage()
        image_path = os.path.join(workdir, self.SubfolderName, self.filename)
        self.showImage(image_path)

    def do_left(self):
        self.pic = self.pic.transpose(Image.ROTATE_90)
        self.saveImage()
        image_path = os.path.join(workdir, self.SubfolderName, self.filename)
        self.showImage(image_path)

    def do_right(self):
        self.pic = self.pic.transpose(Image.ROTATE_270)
        self.saveImage()
        image_path = os.path.join(workdir, self.SubfolderName, self.filename)
        self.showImage(image_path)

    def do_sharp(self):
        self.pic = self.pic.filter(SHARPEN)
        self.saveImage()
        image_path = os.path.join(workdir, self.SubfolderName, self.filename)
        self.showImage(image_path)

    def croppeds(self):
        borders, ok = QInputDialog.getText(wind, 'Введите границы', 'Введите цраницы через запятую.')
        if not ok or not borders:
            return
        try:
            left1, upper, right1, lower = map(int, borders.replace(' ', '').split(','))
            w, h = self.pic.size
            left1, right1 = sorted([max(0, min(left1, w)), max(0, min(right1, w))])
            upper, lower = sorted([max(0, min(upper, h)), max(0, min(lower, h))])
            if right1 == left1:
                right1 += 1
            if lower == upper:
                lower += 1
            box = (left1, upper, right1, lower)
            self.pic = self.pic.crop(box)
            self.saveImage()
            image_path = os.path.join(workdir, self.SubfolderName, self.filename)
            self.showImage(image_path)
        except Exception as error:
            err = QMessageBox()
            err.setText(f'Вводить через запятую.')
            err.exec()
            print(error)

workimage = ImageProcessor()
B_W.clicked.connect(workimage.do_bw)
mirror.clicked.connect(workimage.do_flip)
left.clicked.connect(workimage.do_left)
right.clicked.connect(workimage.do_right)
sharpness.clicked.connect(workimage.do_sharp)
DelButton.clicked.connect(workimage.reset_image)
cropp.clicked.connect(workimage.croppeds)
def showChosenImage():
    if FilesList.currentRow() >= 0:
        filename = FilesList.currentItem().text()
        workimage.loadImage(filename)
        image_path = os.path.join(workdir, workimage.filename)
        workimage.showImage(image_path)

FilesList.currentRowChanged.connect(showChosenImage)

def chooseworkdir():
    global workdir
    workdir = QFileDialog.getExistingDirectory()

def filter(files, extensions):
    result = list()
    for filename in files:
        for extension in extensions:
            if filename.endswith(extension):
                result.append(filename)
    return result

def ShowFilenameList():
    chooseworkdir()
    extensions = ['.jpg', '.png', '.gif', '.bmp', '.jpeg']
    filenames = filter(os.listdir(workdir), extensions)
    FilesList.clear()
    for filename in filenames:
        FilesList.addItem(filename)

PButton.clicked.connect(ShowFilenameList)

wind.show()
app.exec() 

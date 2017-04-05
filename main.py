from PyQt4.QtGui import QWidget, QApplication, QLabel, QPixmap, QVBoxLayout, QFileDialog, QPushButton, QTextEdit, QLineEdit, QHBoxLayout
from PyQt4.QtCore import QObject, SIGNAL
from sys import argv
from PIL import Image, ImageDraw, ImageFont
import random

class interface(QWidget):
    def __init__(self, parent = None):
        QWidget.__init__(self, parent)
        vbox = QVBoxLayout()
        frameLabel = QLabel('Рамка:')
        frameFileDialog = QPushButton("Выбрать рамку...")
        QObject.connect(frameFileDialog, SIGNAL('clicked()'), self.FRAME_FILE_DIALOG)

        bgLabel = QLabel('Фон:')
        bgFileDialog = QPushButton("Выбрать фон...")
        QObject.connect(bgFileDialog, SIGNAL('clicked()'), self.BG_FILE_DIALOG)
        textLabel = QLabel("Текст:")
        self.textEdit = QTextEdit()
        authorLabel = QLabel("Автор:")
        self.authorEdit = QLineEdit()
        saver = QPushButton("Сохранить")
        QObject.connect(saver,SIGNAL('clicked()'), self.callMakeImage)
        vbox.addWidget(frameLabel)
        vbox.addWidget(frameFileDialog)
        vbox.addWidget(bgLabel)
        vbox.addWidget(bgFileDialog)
        vbox.addWidget(textLabel)
        vbox.addWidget(self.textEdit)
        vbox.addWidget(authorLabel)
        vbox.addWidget(self.authorEdit)
        vbox.addWidget(saver)
        hbox = QHBoxLayout()
        hbox.addLayout(vbox)
        self.ready = QLabel()
        hbox.addWidget(self.ready)
        self.setLayout(hbox)
        self.framePath = 'data/Nones/None.png'
        self.bgPath = 'data/Nones/None.png'
        self.SAVE_PATH = 'READYS/' + str(random.randrange(0, 9999)) + '.png'

    def FRAME_FILE_DIALOG(self):
        self.framePath,format = QFileDialog.getOpenFileNameAndFilter(filter='*.png')

    def BG_FILE_DIALOG(self):
        self.bgPath, format= QFileDialog.getOpenFileNameAndFilter(filter="*.jpg *.jpeg *.png *.bmp *.gif")

    def callMakeImage(self):
        self.makeImage(self.framePath, self.bgPath, self.textEdit.toPlainText(), self.authorEdit.text())

    def makeImage(self, frame, backgr, texts, author):
        frame = Image.open(frame)
        backgr = Image.open(backgr)
        texts = texts
        print(frame, backgr, texts, author)

        img1, img2 = frame.resize((720, 480), Image.ANTIALIAS), backgr.resize((720, 480), Image.ANTIALIAS)
        img2.paste(img1, (0, 0), img1)
        draw = ImageDraw.Draw(img2)
        fnt = 14
        sans16 = ImageFont.truetype('fonts/10119.ttf', fnt)
        lineSize = sans16.getsize(texts)
        lines = round((lineSize[0] / 480) + 0.5)
        while(lineSize[1]*lines)<220:
            fnt += 1
            sans16 = ImageFont.truetype('fonts/10119.ttf', fnt)
            lineSize = sans16.getsize(texts)
            lines = round((lineSize[0] / 480) + 0.5)
        print(lineSize)

        print(lines, "   ", len(texts))
        cutForLines = int((len(texts) / lines))
        while cutForLines < len(texts):
            if texts[cutForLines] == ' ':
                texts = texts[:cutForLines] + '\n' + texts[cutForLines + 1:]

            else:
                while texts[cutForLines] != ' ':
                    cutForLines += 1
                    if cutForLines == (len(texts)-1) and texts[cutForLines] !=' ':
                        if texts[cutForLines] != ' ':
                            texts = texts+ ' '
                texts = texts[:cutForLines] + '\n' + texts[cutForLines + 1:]
            cutForLines += int((len(texts) / lines))
        authorSize=sans16.getsize(author)
        draw.text((120, 120), texts, fill=None, font=sans16, anchor=None)
        draw.text((720-(140+authorSize[0]),480-120), author, fill=None, font =sans16, anchor=None)
        img2.save(self.SAVE_PATH)
        self.ready.setPixmap(QPixmap(self.SAVE_PATH))

app = QApplication(argv)
GUI = interface()
GUI.show()
app.exec_()
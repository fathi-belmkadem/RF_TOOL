import sys
import qrc_resources
from PyQt5.QtWidgets import QApplication, QDialog, QWidget
from PyQt5.QtWidgets import QDialogButtonBox, QPushButton, QLabel, QFrame
from PyQt5.QtWidgets import QGridLayout, QVBoxLayout
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas 
import matplotlib.pyplot as plt

class ResultWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__()
        self.setFixedSize(1200, 480)
        #self.setWindowModality(Qt.ApplicationModal)
        self.setWindowTitle("Results")
        self.setWindowIcon(QIcon(":PCB-icon.png"))
        self.dlgLayout = QGridLayout()
        self.dlgLayout.setVerticalSpacing(30)
        self.setLayout(self.dlgLayout)
        self.btn = QPushButton(QIcon(":Accept-icon.png"), " OK")
        self.dlgLayout.addWidget(self.btn, 1, 0, 1, 2, alignment=Qt.AlignBottom | Qt.AlignHCenter)

    def createFrame(self, title, description, image):
        plt.close("all")
        frame = QFrame()
        frame.setFrameShape(QFrame.Panel| QFrame.Sunken)
        frame.setStyleSheet("QFrame {Background-color: white}")
        frame.setLineWidth(3)
        frameLayout = QGridLayout()
        frame.setLayout(frameLayout)
        figure = plt.figure()
        canvas = FigureCanvas(figure)
        ax = figure.add_subplot(111)
        ax.set_xticks([])
        ax.set_yticks([])
        ax.imshow(image, cmap = "gray")
        ttlLabel = QLabel(f"<b>-- {title} --</b>")
        ttlLabel.setStyleSheet("QLabel{color: red}")
        frameLayout.addWidget(ttlLabel, 0, 0, 1, 2, alignment = Qt.AlignHCenter)
        for i, desc in enumerate(description):
            frameLayout.addWidget(QLabel(desc), 1, i, alignment = Qt.AlignHCenter)
        frameLayout.addWidget(canvas, 2, 0, 1, 2, alignment=Qt.AlignHCenter)
        if title.startswith("Solution 1"):
            self.dlgLayout.addWidget(frame, 0, 0)
        elif title.startswith("Solution 2"):
            self.dlgLayout.addWidget(frame, 0, 1)

    def displayDlg(self):
        self.show()
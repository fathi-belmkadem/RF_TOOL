import sys
from brains import calcXYFromZl, caclZlfromXY
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, qApp
from PyQt5.QtWidgets import QHBoxLayout, QLabel
from PyQt5.QtGui import QPixmap, QPen, QPainter, QBrush, QColor
from PyQt5.QtCore import Qt, QPointF, QPoint, pyqtSignal, pyqtSlot

import math, cmath

class SmithChart(QLabel):
    zlMoved = pyqtSignal()
    PADDING = 1
    def __init__(self, dimention=500, parent=None,):
        super().__init__()
        self.DIMENTION = dimention
        #implement mechanism to update z0!!!!!!!!!!!!!!!!!!!
        self.z0 = 50
        self.currentZl = 50
        self.isTracking = True

    def initialize(self):
        self.setFixedSize(self.DIMENTION, self.DIMENTION)
        self.canvas = QPixmap(self.size())
        self.canvas.fill(Qt.white)
        self.drawResistanceCircles()
        self.drawResistanceAxis()
        self.drawReactanceCircles()
        self.plotPointFromZl(self.canvas, Qt.green, self.z0, 0)
        self.setPixmap(self.canvas.scaled(self.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))
        #self.drawArc("resistance", 1+1.5j, 1)
        #self.drawArc("conductance", 3+1j, 1+1.5j)

    def drawResistanceCircles(self):
        painter = QPainter(self.canvas)
        painter.setPen(QPen(QColor("#696968"), .5, Qt.SolidLine))
        painter.setRenderHint(QPainter.Antialiasing, True)
        r_circles = [0, 0.1, 0.3, 0.6, 1, 1.5, 2.4, 4.4, 13]
        # (p - r/(1+r))^2 + q^2 = (1/(1+r))^2
        for r in r_circles:
            radius = round(1/(1+r) * ((self.DIMENTION-2*self.PADDING)/2), 1)
            center = QPointF(round(self.DIMENTION-self.PADDING - radius, 1), round(self.DIMENTION / 2, 1))
            painter.drawEllipse(center, radius, radius)
        painter.end()

    def drawReactanceCircles(self):
        painter = QPainter(self.canvas)
        painter.setPen(QPen(QColor("#696968"), 0.5, Qt.SolidLine))
        painter.setRenderHint(QPainter.Antialiasing, True)
        x_circles = [0.3, 0.6, 1, 1.5, 2.5, 6]
        for x in x_circles:
            # argument of zl = x  (normalized zl)
            # gamma = |gamma|exp(jtheta) = (x - 1)/(x + 1) ==> theta = arctan(-x) - arctan(x)
            theta = math.pi - 2*math.atan(x)
            phi = math.degrees( math.atan(math.sin(theta)/(1-math.cos(theta))) )
            psi = 90 - phi
            start_angle = 2 * psi
            radius = round(1/x * ((self.DIMENTION-2*self.PADDING)/2))
            painter.drawArc(self.DIMENTION-self.PADDING-radius, self.DIMENTION//2 - 2*radius, 2*radius, 2*radius, round((90+start_angle)*16), round((180-start_angle)*16))
            painter.drawArc(self.DIMENTION-self.PADDING-radius, self.DIMENTION//2 , 2*radius, 2*radius, 90*16, round((180-start_angle)*16))
        painter.end()

    def drawResistanceAxis(self):
        painter = QPainter(self.canvas)
        painter.setPen(QPen(Qt.black, 1, Qt.SolidLine))
        painter.setRenderHint(QPainter.Antialiasing, True)
        painter.drawLine(self.DIMENTION - self.PADDING, self.DIMENTION//2, self.PADDING, self.DIMENTION//2) 
        painter.end()

    def mouseMoveEvent(self, e):
        center = (self.DIMENTION-2*self.PADDING)/2
        if math.sqrt((center- e.x())**2 + (center - e.y())**2) <= self.DIMENTION/2:
            Zl = self.calcZl(e.x(), e.y())
            self.plotClickedPoint(Zl)
            self.currentZl = Zl*self.z0
            self.zlMoved.emit()

    def mousePressEvent(self, e):
        self.setPixmap(self.canvas.scaled(self.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))

    def plotPointFromZl(self,paintDev, color, r, react):
        zl = (r + react*1j)/self.z0
        painter = QPainter(paintDev)
        painter.setPen(QPen(color, 5, Qt.SolidLine))
        painter.setRenderHint(QPainter.Antialiasing, True)
        phi = cmath.phase((zl-1)/(zl+1))
        mag = abs((zl-1)/(zl+1))
        x = mag*math.cos(phi) * ((self.DIMENTION-2*self.PADDING)//2)
        y = mag*math.sin(phi) * ((self.DIMENTION-2*self.PADDING)//2)
        painter.drawEllipse(QPointF(self.DIMENTION//2+x, self.DIMENTION//2-y), 2, 2)
        painter.end()
        self.update()

    def plotPointFromXY(self, x, y):
        painter = QPainter(self.pixmap())
        painter.setPen(QPen(Qt.red, 5, Qt.SolidLine))
        painter.setRenderHint(QPainter.Antialiasing, True)
        painter.drawEllipse(x, y, 2, 2)
        painter.end()
        self.update()

    def calcZl(self, x, y):
        p = (x - self.DIMENTION/2) / ((self.DIMENTION - 2*self.PADDING)/2)
        q = (self.DIMENTION/2 -y) / ((self.DIMENTION - 2*self.PADDING)/2)
        R = (1 - p**2 - q**2)/((1 - p)**2 + q**2)
        X = (2*q)/((1 - p)**2 + q**2)
        return R + X*1j

    def plotClickedPoint(self, zl):
        self.setPixmap(self.canvas.scaled(self.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))
        painter = QPainter(self.pixmap())
        painter.setPen(QPen(Qt.red, 2, Qt.SolidLine))
        painter.setRenderHint(QPainter.Antialiasing, True)
        # draw resistance circle
        r_radius = round(1/(1+zl.real) * ((self.DIMENTION-2*self.PADDING)/2), 1)
        r_center = QPointF(round(self.DIMENTION-self.PADDING - r_radius, 1), round(self.DIMENTION / 2, 1))
        painter.drawEllipse(r_center, r_radius, r_radius)
        # draw reactance circle
        if zl.imag != 0:
            theta = math.pi - 2*math.atan(abs(zl.imag))
            phi = math.degrees( math.atan(math.sin(theta)/(1-math.cos(theta))) )
            psi = 90 - phi
            start_angle = 2 * psi
            x_radius = round(1/abs(zl.imag) * ((self.DIMENTION-2*self.PADDING)/2))
            if -2147483648<=x_radius<=2147483647:
                if zl.imag>0:
                    painter.drawArc(self.DIMENTION-self.PADDING-x_radius, self.DIMENTION//2 - 2*x_radius, 2*x_radius, 2*x_radius, round((90+start_angle)*16), round((180-start_angle)*16))
                elif zl.imag<0:
                    painter.drawArc(self.DIMENTION-self.PADDING-x_radius, self.DIMENTION//2 , 2*x_radius, 2*x_radius, 90*16, round((180-start_angle)*16))
        painter.end()
        self.plotPointFromZl(self.pixmap(), Qt.red, zl.real*self.z0, zl.imag*self.z0)
        self.update()

    def calcZDeltaPhi(self, zl1, zl2):
        radius = 1/(1+zl1.real) * ((self.DIMENTION-2*self.PADDING)/2)
        center = QPointF(self.DIMENTION-self.PADDING - radius, self.DIMENTION / 2)
        x1, y1 = calcXYFromZl(zl1)
        x2, y2 = calcXYFromZl(zl2)
        x1 = x1 - (center.x() - self.DIMENTION/2)/((self.DIMENTION-2*self.PADDING)/2)
        x2 = x2 - (center.x() - self.DIMENTION/2)/((self.DIMENTION-2*self.PADDING)/2)
        z1 = x1 + y1*1j
        z2 = x2 + y2*1j
        phi1 = math.degrees(cmath.phase(z1)) % 360
        phi2 = math.degrees(cmath.phase(z2)) % 360
        return phi1, phi2 - phi1
        
    def calcYDeltaPhi(self, yl1, yl2):
        radius = 1/(1+yl1.real) * ((self.DIMENTION-2*self.PADDING)/2)
        center = QPointF(round(self.DIMENTION-self.PADDING - radius, 1), round(self.DIMENTION / 2, 1))
        zl1 = 1/yl1
        zl2 = 1/yl2
        x1, y1 = calcXYFromZl(zl1)
        x2, y2 = calcXYFromZl(zl2)
        x1 = x1 + (center.x() - self.DIMENTION/2)/((self.DIMENTION-2*self.PADDING)/2)
        x2 = x2 + (center.x() - self.DIMENTION/2)/((self.DIMENTION-2*self.PADDING)/2)
        # z1 & z2 are the new coords of zl1, zl2
        z1 = x1 + y1*1j
        z2 = x2 + y2*1j
        phi1 = math.degrees(cmath.phase(z1))
        phi2 = math.degrees(cmath.phase(z2))
        return phi1, phi2 - phi1
        
    def drawArc(self, name, color, zl1, zl2):
        painter = QPainter(self.pixmap())
        painter.setPen(QPen(color, 3, Qt.SolidLine))
        painter.setRenderHint(QPainter.Antialiasing, True)
        if name == "resistance":
            radius = round(1/(1+zl1.real) * ((self.DIMENTION-2*self.PADDING)/2))
            start_angle, span_angle = self.calcZDeltaPhi(zl1, zl2)
            x, y  = self.DIMENTION-self.PADDING - 2*radius, self.DIMENTION / 2 - radius
            painter.drawArc(round(x), round(y), 2*radius, 2*radius, round(start_angle*16), round(span_angle*16))
        elif name == "conductance":
            yl1 = 1/zl1
            yl2 = 1/zl2
            radius = round(1/(1+yl1.real) * ((self.DIMENTION-2*self.PADDING)/2))
            start_angle, span_angle = self.calcYDeltaPhi(yl1, yl2)
            x, y  = self.PADDING, self.DIMENTION / 2 - radius
            painter.drawArc(round(x), round(y), 2*radius, 2*radius, round(start_angle*16), round(span_angle*16))
        painter.end()
        self.plotPointFromZl(self.pixmap(), Qt.blue, zl2.real*self.z0, zl2.imag*self.z0)
        self.update()

    @pyqtSlot()
    def updateFields(self, rlField, xlField, magField, phiField):
        gamma = (self.currentZl/50 - 1)/(self.currentZl/50 + 1)
        rlField.setText("{:.3e}".format(self.currentZl.real))
        xlField.setText("{:.3e}".format(self.currentZl.imag))
        magField.setText("{:.3e}".format(abs(gamma)))
        phiField.setText("{:.3e}".format(math.degrees(cmath.phase(gamma)) % 360))
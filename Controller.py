import cmath, math
from functools import partial
from ResultWindowUI import ResultWindow
from brains import calcZlFromGamma, makeErrMsg
from PyQt5.QtCore import Qt
from MainWindowUI import Card
class Ctrl:
    def __init__(self, model, view):
        self._view = view
        self._model = model
        self._resWindow = ResultWindow(parent = self._view)
        self._connectSignals()

    def _calculateResults(self):
        f = self._view.getF()
        z0 = self._view.getZ0()
        if self._view.inputChoice.currentText() == "Complex Load":
            rl = self._view.getRL()
            xl = self._view.getXL()
            res = self._model.calcFromZL(f, z0, rl, xl)
        elif self._view.inputChoice.currentText() == "S-Parameter / Reflection coefficient":
            mag = self._view.getMag()
            phi = self._view.getPhi()
            res = self._model.calcFromGamma(f, z0, mag, phi)
        return res

    def drawOnSmith(self, results):
        units ={'': 0, 'm': -3, 'μ': -6, 'n': -9, 'p': -12, 'f': -15}
        for color, res in zip((Qt.yellow, Qt.green), results.values()):
            z1 = self._view.p1SmithChart.currentZl
            for comp in res[::-1]:
                val = comp.value
                if comp.categ == "capacitor":
                    val = 1/(val*10**units[comp.unit[0]]*2*math.pi*self._view.getF()*1j)
                    if comp.config == "series":
                        z2 = (z1 + val) / self._view.getZ0()
                        self._view.p1SmithChart.drawArc("resistance", color, z1 / self._view.getZ0(), z2)
                    if comp.config == "parallel":
                        z2 = 1/(1/z1 + 1/val) / self._view.getZ0()
                        self._view.p1SmithChart.drawArc("conductance", color, z1 / self._view.getZ0(), z2)
                elif comp.categ == "inductor":
                    val = val*10**units[comp.unit[0]]*2*math.pi*self._view.getF()*1j
                    if comp.config == "series":
                        z2 = (z1 + val) / self._view.getZ0()
                        self._view.p1SmithChart.drawArc("resistance", color, z1 / self._view.getZ0(), z2)
                    if comp.config == "parallel":
                        z2 = 1/(1/z1 + 1/val) / self._view.getZ0()
                        self._view.p1SmithChart.drawArc("conductance", color, z1 / self._view.getZ0(), z2)
                z1 = z2 * self._view.getZ0()


    def _displayResults(self):
        if self._view.inputChoice.currentIndex() == 0:
            fields = [(self._view.f, self._view.fWarning), (self._view.z0, self._view.z0Warning), (self._view.rl, self._view.rlWarning), (self._view.xl, self._view.xlWarning)]
        else:
            fields = [(self._view.f, self._view.fWarning), (self._view.z0, self._view.z0Warning) , (self._view.mag, self._view.magWarning), (self._view.phi, self._view.phiWarning)]
        if all([field[0].text() != "" and field[1].text() == "" for field in fields]):
            results = self._calculateResults()
            for k, v in results.items():
                description, circuit = self._model.buildCircuit(v)
                if k == 'sol1':
                    title = "Solution 1"
                else:
                    title = "Solution 2"
                self._resWindow.createFrame(title, description, circuit)
            self.drawOnSmith(results)
            self._resWindow.displayDlg()

    def _connectSignals(self):
        self._view.btn.clicked.connect(partial(self._displayResults))
        self._view.f.textEdited.connect(partial(self.checker, self._view.f, self._view.fWarning, inf=0.0 , sup=None))
        self._view.z0.textEdited.connect(partial(self.checker, self._view.z0, self._view.z0Warning, inf=0.0, sup=None))
        self._view.rl.textEdited.connect(partial(self.checker, self._view.rl, self._view.rlWarning, inf=0.0, sup=None))
        self._view.xl.textEdited.connect(partial(self.checker, self._view.xl, self._view.xlWarning, inf=None, sup=None))
        self._view.mag.textEdited.connect(partial(self.checker, self._view.mag, self._view.magWarning, inf=0.0, sup=1.0))
        self._view.phi.textEdited.connect(partial(self.checker, self._view.phi, self._view.phiWarning, inf=0, sup=360))
        self._resWindow.btn.clicked.connect(self._resWindow.close)
        #page2
        for btn in self._view.p2btns:
            btn.clicked.connect(partial(self.addCard, btn.text()))
        self._view.p2z0.textEdited.connect(self.updateSmith2)
        self._view.p2f.textEdited.connect(self.updateSmith2)
        self._view.load.rl.textEdited.connect(self.updateSmith2)
        self._view.load.xl.textEdited.connect(self.updateSmith2)
        self._view.magF.currentIndexChanged.connect(self.updateSmith2)

    def updateSmith1(self, rl, xl):
        self._view.p1SmithChart.currentZl = rl + xl*1j
        rl = rl / self._view.getZ0()
        xl = xl / self._view.getZ0()
        self._view.p1SmithChart.plotClickedPoint(rl + xl*1j)

    def checker(self, fieldName, fieldWarning, inf=None, sup=None):
        expression = fieldName.text()
        errMsg = makeErrMsg(expression, inf, sup)
        if errMsg == "":
            if fieldName in {self._view.rl, self._view.xl} and self._view.rl.text() != "" and self._view.xl.text() != "":
                self.updateSmith1(self._view.getRL(), self._view.getXL())
            elif fieldName in {self._view.phi, self._view.mag} and self._view.mag.text() != "" and self._view.phi.text() != "":
                rl, xl = calcZlFromGamma(self._view.getMag(), self._view.getPhi())
                self.updateSmith1(rl*self._view.getZ0(), xl*self._view.getZ0())
            elif fieldName == self._view.z0:
                self._view.p1SmithChart.z0 = self._view.getZ0()
            fieldWarning.setFixedHeight(0)
        else:
            fieldWarning.setFixedHeight(16)
        fieldWarning.setText(errMsg)

    #page2
    cards = []
    zList = []
    def addCard(self, categ):
        if len(self.cards) < 10:
            card = Card(categ)
            self._view.circuitLayout.insertWidget(len(self.cards)+1, card, stretch=0, alignment=Qt.AlignLeft)
            self.cards.append(card)
            card.val.textEdited.connect(self.updateSmith2)
            card.unit.currentTextChanged.connect(self.updateSmith2)
            card.delbtn.clicked.connect(partial(self.delCard, card))
            self.updateSmith2()

    def delCard(self, card):
        child =self._view.circuitLayout.takeAt(self.cards.index(card)+1)
        self.cards.remove(card)
        if child.widget():
            child.widget().deleteLater()
        self.updateSmith2()

    def updateSmith2(self):
        if makeErrMsg(self._view.load.rl.text(), 0) != "" or makeErrMsg(self._view.load.xl.text()) != "" or makeErrMsg(self._view.p2f.text(), 0)!= "" or makeErrMsg(self._view.p2z0.text(), 0)!="":
            return None
        smithChart = self._view.p2SmithChart
        smithChart.currentZl = self._view.p2getz0()
        smithChart.setPixmap(smithChart.canvas.scaled(smithChart.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))
        self.zList = [self._view.p2getRL() + self._view.p2getXL()*1j]
        for i, c in enumerate(self.cards):
            config, categ = c.categ.split()
            f = self._view.p2getF()
            try:
                c.getVal()
            except:
                break
            if c.getVal()==0:
                break
            if categ == "capacitor":
                z = 1/(2*math.pi*f*c.getVal()*1j)
                if config == "series":
                    self.zList.append(self.zList[-1] + z)
                    smithChart.drawArc("resistance", Qt.blue, self.zList[i]/self._view.p2getz0(), self.zList[i+1]/self._view.p2getz0())
                elif config == "parallel":
                    self.zList.append(1/(1/self.zList[-1] + 1/z))
                    smithChart.drawArc("conductance", Qt.blue, self.zList[i]/self._view.p2getz0(), self.zList[i+1]/self._view.p2getz0())
            elif categ == "inductor":
                z = 2*math.pi*f*c.getVal()*1j
                if config == "series":
                    self.zList.append(self.zList[-1] + z)
                    smithChart.drawArc("resistance", Qt.blue, self.zList[i]/self._view.p2getz0(), self.zList[i+1]/self._view.p2getz0())
                elif config == "parallel":
                    self.zList.append(1/(1/self.zList[-1] + 1/z))
                    smithChart.drawArc("conductance", Qt.blue, self.zList[i]/self._view.p2getz0(), self.zList[i+1]/self._view.p2getz0())


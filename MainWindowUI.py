import sys
from functools import partial
import qrc_resources
from smith import SmithChart
from brains import calcZlFromGamma
from PyQt5.QtWidgets import QWidget, QMainWindow
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QGridLayout, QScrollArea
from PyQt5.QtWidgets import QTabWidget, QStackedWidget, QFrame, QGroupBox
from PyQt5.QtWidgets import QPushButton, QLabel, QComboBox, QLineEdit
from PyQt5.QtWidgets import QToolBar, QStatusBar, QMenuBar, QMenu, QAction
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QKeySequence, QPixmap, QColor, qRgb

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowTitle("RF Tool")
        self.setWindowIcon(QIcon(":icon.png"))
        self.move(300, 50)
        self._centralWidget = QWidget()
        self.centralWidgetLayout = QHBoxLayout()
        self.centralWidgetLayout.setContentsMargins(0,0,0,0)
        self._centralWidget.setLayout(self.centralWidgetLayout)
        self.setCentralWidget(self._centralWidget)
        self._buildUI()

    def _buildUI(self):
        self._createActions()
        self._createMenuBar()
        self._createToolBar()
        self._createStatusBar()
        self._connectActions()
        self._buildCentralWidget()

    def _createMenuBar(self):
        menuBar = self.menuBar()
        # file menu
        self.fileMenu = menuBar.addMenu("&File")
        self.fileMenu.addAction(self.newAction)
        self.fileMenu.addAction(self.openAction)
        self.fileMenu.addAction(self.saveAction)
        self.fileMenu.addSeparator()
        self.fileMenu.addAction(self.exitAction)
        # edit menu
        self.editMenu = menuBar.addMenu("&Edit")
        self.editMenu.addAction(self.undoAction)
        self.editMenu.addAction(self.redoAction)
        self.editMenu.addSeparator()
        self.editMenu.addAction(self.cutAction)
        self.editMenu.addAction(self.copyAction)
        self.editMenu.addAction(self.pasteAction)
        self.editMenu.addSeparator()
        findReplaceMenu = QMenu("&Find && Replace...")
        findReplaceMenu.addAction(self.findAction)
        findReplaceMenu.addAction(self.replaceAction)
        self.editMenu.addMenu(findReplaceMenu)
        # preferences menu
        self.preferencesMenu = menuBar.addMenu("&Preferences")
        self.preferencesMenu.addAction(self.settingsAction)
        # help menu
        self.helpMenu = menuBar.addMenu(QIcon(":help-icon.png"), "&Help")
        self.helpMenu.addActions([self.helpContentAction, self.aboutAction])

    def _createToolBar(self):
        # file toolbar
        fileToolBar = QToolBar("File", self)
        fileToolBar.addActions([self.newAction, self.openAction, self.saveAction])
        fileToolBar.addSeparator()
        fileToolBar.addAction(self.exitAction)
        # edit toolbar
        editToolBar = QToolBar("Edit", self)
        editToolBar.addActions([self.undoAction, self.redoAction])
        editToolBar.addSeparator()
        editToolBar.addActions([self.cutAction, self.copyAction, self.pasteAction])
            # add QLineedit for findAction
            # add 2xQLineEdit  for replace action
        # preferences toolbar
        preferencesToolBar = QToolBar("preferences", self)
        preferencesToolBar.addAction(self.settingsAction)
        # 
        self.addToolBar(Qt.TopToolBarArea, fileToolBar)
        self.addToolBar(Qt.TopToolBarArea, editToolBar)
        self.addToolBar(Qt.TopToolBarArea, preferencesToolBar)
        # configuring  toolbars
        fileToolBar.setFloatable(False)
        editToolBar.setFloatable(False)
        preferencesToolBar.setFloatable(False)

    def _createActions(self): 
        # file actions
        self.newAction = QAction(QIcon(":New-file-icon.png"), "&New", self)
        self.newAction.setShortcut(QKeySequence.New)
        self.newAction.setToolTip("new")
        self.newAction.setStatusTip("Open a new blank file")

        self.openAction = QAction(QIcon(":Open-file-icon.png"), "&Open...", self)
        self.openAction.setShortcut(QKeySequence.Open)
        self.openAction.setToolTip("Open")
        self.openAction.setStatusTip("Open a file")

        self.saveAction = QAction(QIcon(":Save-icon.png"), "&Save", self)
        self.saveAction.setShortcut(QKeySequence.Save)
        self.saveAction.setToolTip("Save")
        self.saveAction.setStatusTip("Save file")

        self.exitAction = QAction(QIcon(":Exit-icon.png"), "&Exit", self)
        self.exitAction.setShortcut("Alt+F4")
        self.exitAction.setToolTip("exit")
        self.exitAction.setStatusTip("exit program")
        # edit actions
        self.undoAction = QAction(QIcon(":Undo-icon.png"), "&Undo", self)
        self.undoAction.setShortcut(QKeySequence.Undo)
        self.undoAction.setToolTip("Undo")
        self.undoAction.setStatusTip("Undo latest action")

        self.redoAction = QAction(QIcon(":Redo-icon.png"), "&Redo", self)
        self.redoAction.setShortcut(QKeySequence.Redo)
        self.redoAction.setToolTip("Redo")
        self.redoAction.setStatusTip("Redo action")

        self.cutAction = QAction(QIcon(":Cut-icon.png"), "Cu&t               ", self)
        self.cutAction.setShortcut(QKeySequence.Cut)
        self.cutAction.setToolTip("Cut")
        self.cutAction.setStatusTip("Cut selected content to clipboard")

        self.copyAction = QAction(QIcon(":Copy-icon.png"), "&Copy", self)
        self.copyAction.setShortcut(QKeySequence.Copy)
        self.copyAction.setToolTip("Copy")
        self.copyAction.setStatusTip("Copy selected content to clipBoard")

        self.pasteAction = QAction(QIcon(":Paste-icon.png"), "&Paste", self)
        self.pasteAction.setShortcut(QKeySequence.Paste)
        self.pasteAction.setToolTip("Paste")
        self.pasteAction.setStatusTip("Paste content from clipboard")

        self.findAction = QAction("&Find", self)
        self.findAction.setShortcut(QKeySequence.Find)
        self.findAction.setToolTip("Find")
        self.findAction.setStatusTip("Find content")

        self.replaceAction = QAction("&Replace", self)
        # preferences actions
        self.settingsAction = QAction(QIcon(":Settings-icon.png"), "&Settings", self)
        self.settingsAction.setShortcut("Ctrl+,")
        self.settingsAction.setToolTip("Settings")
        self.settingsAction.setStatusTip("Access user settings")
        # help actions
        self.helpContentAction = QAction(QIcon(":Help-contents-icon.png"), "&Help Content...", self)
        self.helpContentAction.setShortcut(QKeySequence.HelpContents)
        self.helpContentAction.setToolTip("More about the subject")
        self.helpContentAction.setStatusTip("More about the subject")

        self.aboutAction = QAction(QIcon(":About-icon.png"), "&About...", self)
        self.aboutAction.setShortcut("Ctrl+A")
        self.aboutAction.setToolTip("About this program")
        self.aboutAction.setStatusTip("About this program")

    def _createStatusBar(self):
        self.statusBar = self.statusBar()
        self.statusBar.showMessage("ready", 5000)

    def contextMenuEvent(self, event):
        menu = QMenu(self._centralWidget)
        menu.addAction(self.newAction)
        menu.addAction(self.openAction)
        menu.addAction(self.saveAction)
        menu.addSeparator()
        menu.addAction(self.undoAction)
        menu.addAction(self.redoAction)
        menu.addSeparator()
        menu.addAction(self.cutAction)
        menu.addAction(self.copyAction)
        menu.addAction(self.pasteAction)
        menu.exec(event.globalPos())

    def newFile(self):
        self.statusBar.showMessage("File > New clicked", 3000)

    def openFile(self):
        self.statusBar.showMessage("File > Open... clicked", 3000)

    def saveFile(self):
        self.statusBar.showMessage("File > Save clicked", 3000)

    def undoActivity(self):
        self.statusBar.showMessage("Edit > Undo clicked", 3000)

    def redoActivity(self):
        self.statusBar.showMessage("Edit > Redo clicked", 3000)

    def cutContent(self):
        self.statusBar.showMessage("Edit > Cut clicked", 3000)

    def copyContent(self):
        self.statusBar.showMessage("Edit > Copy clicked", 3000)

    def pasteContent(self):
        self.statusBar.showMessage("Edit > paste clicked", 3000)

    def openSettingsWindow(self):
        self.statusBar.showMessage("Preferences > Settings clicked", 3000)

    def helpContent(self):
        self.statusBar.showMessage("Help > helpContent clicked", 3000)

    def about(self):
        self.statusBar.showMessage("Help > About clicked", 3000)

    def _connectActions(self):
        # connecting file actions
        self.newAction.triggered.connect(self.newFile)
        self.openAction.triggered.connect(self.openFile)
        self.saveAction.triggered.connect(self.saveFile)
        self.exitAction.triggered.connect(self.close)
        # connecting edit actions
        self.undoAction.triggered.connect(self.undoActivity)
        self.redoAction.triggered.connect(self.redoActivity)
        self.cutAction.triggered.connect(self.cutContent)
        self.copyAction.triggered.connect(self.copyContent)
        self.pasteAction.triggered.connect(self.pasteContent)
        # connecting preferences actions
        self.settingsAction.triggered.connect(self.openSettingsWindow)
        # connecting help actions
        self.helpContentAction.triggered.connect(self.helpContent)
        self.aboutAction.triggered.connect(self.about)

    def _buildCentralWidget(self):
        self._centralWidget = QWidget()
        self._centralWidgetLayout = QHBoxLayout()
        self._centralWidget.setLayout(self._centralWidgetLayout)
        self.setCentralWidget(self._centralWidget)
        self._createTabs()
        #self._createFrame()

    def _buildPage1(self):
        page1 = QWidget()
        p1Layout = QHBoxLayout()
        smithFrame = QFrame()
        smithFrame.setFrameShape(QFrame.StyledPanel | QFrame.Plain)
        smithFrame.setStyleSheet("QFrame {background: white}")
        smithFrameLayout = QHBoxLayout()
        self.p1SmithChart = SmithChart(dimention=700)
        self.p1SmithChart.initialize()
        smithFrameLayout.addWidget(self.p1SmithChart)
        smithFrame.setLayout(smithFrameLayout)
        p1Layout.addWidget(smithFrame)
        self.inputFrame = self._createInputFrame()
        p1Layout.addWidget(self.inputFrame)
        page1.setLayout(p1Layout)
        self.p1SmithChart.zlMoved.connect(partial(self.p1SmithChart.updateFields, self.rl, self.xl, self.mag, self.phi))
        return page1
        
    def _buildPage2(self):
        page2 = QWidget()
        p2Layout = QGridLayout()
        z0Label = QLabel("Z0")
        fLabel = QLabel("   frequency")
        self.p2z0 = QLineEdit("50")
        self.p2f = QLineEdit("10")
        self.magF = QComboBox()
        self.magF.addItems(['Hz', 'KHz', 'MHz', 'GHz', 'THz'])
        self.magF.setCurrentIndex(2)
        group = QGroupBox()
        glayout = QHBoxLayout()
        glayout.addWidget(z0Label)
        glayout.addWidget(self.p2z0)
        glayout.addWidget(fLabel)
        glayout.addWidget(self.p2f)
        glayout.addWidget(self.magF)
        group.setLayout(glayout)
        group.setFixedSize(400, 40)
        smithFrame = QFrame()
        smithFrame.setFrameShape(QFrame.StyledPanel | QFrame.Plain)
        smithFrame.setStyleSheet("QFrame {background: white}")
        smithFrameLayout = QHBoxLayout()
        self.p2SmithChart = SmithChart(dimention=500)
        self.p2SmithChart.initialize()
        #self.polarChart = PolarChart()
        #self.polarChart.initialize()
        smithFrameLayout.addWidget(self.p2SmithChart, alignment=Qt.AlignHCenter | Qt.AlignVCenter)
        #smithFrameLayout.addWidget(self.polarChart, alignment =Qt.AlignHCenter | Qt.AlignVCenter)
        smithFrame.setLayout(smithFrameLayout)
        p2Layout.addWidget(smithFrame, 0, 0, 1, 2)
        self.circuitFrame = QFrame()
        self.circuitFrame.setFrameShape(QFrame.Panel | QFrame.Plain)
        self.circuitFrame.setStyleSheet("QFrame {background: white}")
        self.circuitLayout = QHBoxLayout()
        self.circuitFrame.setLayout(self.circuitLayout)
        self.load = Card("reverse load")
        self.circuitLayout.addWidget(self.load, alignment=Qt.AlignLeft, stretch=0)
        self.circuitLayout.addStretch()
        #scroll = QScrollArea()
        #scroll.setWidget(self.circuitFrame)
        #scroll.setWidgetResizable(True)
        #scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        #scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        btnFrame = QFrame()
        btnFrame.setFixedSize(300, 200)
        btnFrame.setFrameShape(QFrame.Panel | QFrame.Plain)
        btnLayout = QGridLayout()
        addSeriesC = QPushButton(QIcon(":Add-icon.png"), "series capacitor")
        addShuntC = QPushButton(QIcon(":Add-icon.png"), "parallel capacitor")
        addSeriesL = QPushButton(QIcon(":Add-icon.png"), "series inductor")
        addShuntL = QPushButton(QIcon(":Add-icon.png"), "parallel inductor")
        self.p2btns = [addSeriesC, addSeriesL, addShuntC, addShuntL]
        hSeparator = QFrame()
        vSeparator = QFrame()
        hSeparator.setFrameShape(QFrame.HLine | QFrame.Raised)
        vSeparator.setFrameShape(QFrame.VLine | QFrame.Raised)
        btnLayout.addWidget(addSeriesC, 0, 0)
        btnLayout.addWidget(addShuntC, 0, 2)
        btnLayout.addWidget(addSeriesL, 2, 0)
        btnLayout.addWidget(addShuntL, 2, 2)
        btnLayout.addWidget(hSeparator, 1, 0, 1, 3)
        btnLayout.addWidget(vSeparator, 0, 1, 3, 1)
        btnLayout.setVerticalSpacing(0)
        btnFrame.setLayout(btnLayout)
        p2Layout.addWidget(group, 1, 0)
        p2Layout.addWidget(self.circuitFrame, 2, 0)
        p2Layout.addWidget(btnFrame, 2, 1)
        #p2Layout.addWidget(scroll, 2, 0, 1, 2)
        p2Layout.setHorizontalSpacing(0)
        page2.setLayout(p2Layout)
        return page2

    def _createTabs(self):
        self.tabs = QTabWidget()
        page1 = self._buildPage1()
        page2 = self._buildPage2()
        page1.setAutoFillBackground(True)
        page2.setAutoFillBackground(True)
        self.tabs.addTab(page1, "auto")
        self.tabs.addTab(page2, "custom")
        self._centralWidgetLayout.addWidget(self.tabs)
        
    def _createInputFrame(self):
        self.frame = QFrame()
        self.frame.setFrameShape(QFrame.Panel | QFrame.Sunken)
        self.frame.setFixedWidth(400)
        self.frame.setLineWidth(3)
        self.frameLayout = QVBoxLayout()
        self.frame.setLayout(self.frameLayout)
        # frequency Group
        fGroup = QGroupBox("Operating frequency")
        self.fGroupLayout = QGridLayout()
        self.f = QLineEdit()
        self.f.setPlaceholderText("frequency")
        self.f.setToolTip("frequency")
        self.fWarning = QLabel("")
        self.fWarning.setStyleSheet("QLabel {color: red}")
        self.fWarning.setFixedHeight(0)
        self.fmagComboBox = QComboBox()
        self.fmagComboBox.addItems(["Hz", "KHz", "MHz", "GHz", "THz"])
        self.fmagComboBox.setCurrentIndex(2)
        self.fGroupLayout.addWidget(self.f, 0, 0)
        self.fGroupLayout.addWidget(self.fmagComboBox, 0, 1)
        self.fGroupLayout.addWidget(self.fWarning, 2, 0, 1, 2)
        fGroup.setLayout(self.fGroupLayout)
        # Characteristic impedence group
        z0Group = QGroupBox("Characteristic Impedence (Ohms Ω)")
        self.z0 = QLineEdit("50")
        self.z0.setPlaceholderText("example: 50Ω")
        self.z0.setToolTip("Zc")
        self.z0Warning = QLabel("")
        self.z0Warning.setFixedHeight(0)
        self.z0Warning.setStyleSheet("QLabel {color: red}")
        self.z0Layout = QVBoxLayout()
        self.z0Layout.addWidget(self.z0)
        self.z0Layout.addWidget(self.z0Warning)
        z0Group.setLayout(self.z0Layout)
        # choice of input type: "Complex Load" or "S-Parameters"
        self.stackedWidget = QStackedWidget()
        choiceLabel = QLabel("InputType:")
        self.inputChoice = QComboBox()
        self.inputChoice.addItems(["Complex Load", "S-Parameter / Reflection coefficient"])
        self.inputChoice.activated.connect(self.switchInput)
        # Complex Load group
        zlPage = QWidget()
        zlPageLayout = QVBoxLayout()
        zlGroup = QGroupBox("Load Impedence (Ohms Ω)")
        self.zlLayout = QGridLayout()

        self.rl = QLineEdit()
        self.rl.setPlaceholderText("Resistance")
        self.rl.setToolTip("RL")
        self.rlWarning = QLabel("")
        self.rlWarning.setFixedHeight(0)
        self.rlWarning.setStyleSheet("QLabel {color: red}")


        self.xl = QLineEdit()
        self.xl.setPlaceholderText("Reactance")
        self.xl.setToolTip("XL")
        self.xlWarning = QLabel("")
        self.xlWarning.setFixedHeight(0)
        self.xlWarning.setStyleSheet("QLabel {color: red}")
        jLabel = QLabel("    +    <b>j</b>")

        self.zlLayout.addWidget(self.rl, 0, 0)
        self.zlLayout.addWidget(jLabel, 0, 1)
        self.zlLayout.addWidget(self.xl, 0, 2)
        self.zlLayout.addWidget(self.rlWarning, 1, 0)
        self.zlLayout.addWidget(self.xlWarning, 1, 2)
        zlGroup.setLayout(self.zlLayout)
        zlPageLayout.addWidget(zlGroup)
        zlPageLayout.addStretch()
        zlPage.setLayout(zlPageLayout)
        # S-Parameters groups
        spPage = QWidget()
        spPageLayout = QVBoxLayout()
        spGroup = QGroupBox("S-Parameter")
        spLayout = QVBoxLayout()

        magGroup = QGroupBox("Magnitude")
        self.magLayout = QVBoxLayout()
        self.mag = QLineEdit()
        self.mag.setPlaceholderText("0.0 ≤ Magnitude ≤ 1.0")
        self.mag.setToolTip("magnitude of Gamma")
        self.magWarning = QLabel("")
        self.magWarning.setFixedHeight(0)
        self.magWarning.setStyleSheet("QLabel {color: red}")
        self.magLayout.addWidget(self.mag)
        self.magLayout.addWidget(self.magWarning)
        magGroup.setLayout(self.magLayout)

        phiGroup = QGroupBox("Phase φ (Degrees)")
        self.phiLayout = QVBoxLayout()
        self.phi = QLineEdit()
        self.phi.setPlaceholderText("0° ≤ φ ≤ 360°")
        self.phi.setToolTip("phase of Gamma")
        self.phiWarning = QLabel("")
        self.phiWarning.setFixedHeight(0)
        self.phiWarning.setStyleSheet("QLabel {color: red}")
        self.phiLayout.addWidget(self.phi)
        self.phiLayout.addWidget(self.phiWarning)
        phiGroup.setLayout(self.phiLayout)

        spLayout.addWidget(magGroup)
        spLayout.addWidget(phiGroup)
        spGroup.setLayout(spLayout)
        spPageLayout.addWidget(magGroup)
        spPageLayout.addWidget(phiGroup)
        spPageLayout.addStretch()
        spPage.setLayout(spPageLayout)
        # Adding choices to stackedFrame
        self.stackedWidget.addWidget(zlPage)
        self.stackedWidget.addWidget(spPage)
        # button
        self.btn = QPushButton(QIcon(":Calculator-icon.png"), " Calculate")
        self.btn.setToolTip("Click to generate maching networks")
        # populating frame layout
        self.frameLayout.addWidget(fGroup)
        self.frameLayout.addWidget(z0Group)
        self.frameLayout.addSpacing(15)
        self.frameLayout.addWidget(choiceLabel)
        self.frameLayout.addWidget(self.inputChoice)
        self.frameLayout.addSpacing(10)
        self.frameLayout.addWidget(self.stackedWidget)
        self.frameLayout.addWidget(self.btn, alignment= Qt.AlignBottom | Qt.AlignLeft)
        # positioning frame in central widget
        #self._centralWidgetLayout.addWidget(self.frame, alignment= Qt.AlignRight)
        return self.frame

    def switchInput(self):
        self.stackedWidget.setCurrentIndex(self.inputChoice.currentIndex())

    #public API
    def getF(self):
        magDict = {"Hz": 0, "KHz": 3, "MHz": 6, "GHz": 9, "THz": 12}
        f = float(self.f.text())
        mag = self.fmagComboBox.currentText()
        return f * 10**magDict[mag]

    def getZ0(self):
        return float(self.z0.text())

    def getRL(self):
        return float(self.rl.text())

    def getXL(self):
        return float(self.xl.text())

    def getMag(self):
        return float(self.mag.text())

    def getPhi(self):
        return float(self.phi.text())   

    def p2getF(self):
        units = {'Hz': 0, 'KHz': 3, 'MHz': 6, 'GHz': 9, 'THz': 12}
        return float(self.p2f.text()) * 10**units[self.magF.currentText()]

    def p2getz0(self):
        return float(self.p2z0.text())

    def p2getRL(self):
        return float(self.load.rl.text())

    def p2getXL(self):
        return float(self.load.xl.text())

class Card(QFrame):
    unitsF = {"F": 0, "mF": -3, "uF": -6, "nF": -9, "pF": -12, "fF": -15}
    unitsH = {"H": 0, "mH": -3, "uH": -6, "nH": -9, "pH": -12, "fH": -15}

    def __init__(self, categ):
        super().__init__()
        self.categ = categ
        self.setFrameShape(QFrame.StyledPanel | QFrame.Plain)
        label = QLabel()
        label.setFixedSize(120, 100)
        canvas = QPixmap("resources/components/{}.png".format(self.categ))
        label.setPixmap(canvas)
        label.setScaledContents(True)
        cardLayout = QVBoxLayout()
        inputLayout = QHBoxLayout()
        if self.categ != "reverse load":
            self.val = QLineEdit("1")
            self.val.setFixedWidth(69)
            if "capacitor" in self.categ:
                self.units = self.unitsF
            elif "inductor" in self.categ:
                self.units = self.unitsH
            self.unit = QComboBox()
            self.unit.addItems(self.units.keys())
            self.unit.setCurrentIndex(3)
            self.unit.setFixedWidth(45)
            inputLayout.addWidget(self.val)
            inputLayout.addWidget(self.unit)
        else:
            j = QLabel("+j")
            self.xl = QLineEdit("0")
            self.rl = QLineEdit("50")
            self.xl.setFixedWidth(50)
            self.rl.setFixedWidth(50)
            inputLayout.addWidget(self.rl)
            inputLayout.addWidget(j)
            inputLayout.addWidget(self.xl)
            inputLayout.setSpacing(0)
        cardLayout.addWidget(label)
        cardLayout.addLayout(inputLayout)
        if categ != "reverse load":
            self.delbtn = QPushButton(QIcon(":Recycle-icon.png"), "")
            self.delbtn.setToolTip("remove card")
            cardLayout.addWidget(self.delbtn)
        else:
            btn = QPushButton(QIcon(":Denied-icon.png"), "")
            btn.setToolTip("cannot remove this card")
            cardLayout.addWidget(btn)
        cardLayout.setContentsMargins(5, 5, 5, 5)
        self.setLayout(cardLayout)

    def getVal(self):
        return float(self.val.text()) * 10**self.units[self.unit.currentText()]

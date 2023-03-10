import sys
from MainWindowUI import MainWindow
from Controller import Ctrl
import brains
from PyQt5.QtWidgets import QApplication

def main():
    app = QApplication(sys.argv)
    homePage = MainWindow()
    Ctrl(brains, homePage)
    homePage.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
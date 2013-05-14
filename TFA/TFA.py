from PyQt4.QtCore import *
from PyQt4.QtGui import *
from viewClass import view
import sys


class mainWindow(QMainWindow):
    def __init__(self):
        super(mainWindow,self).__init__()
        self.setWindowTitle("Trans Fat Assassin")
        #self.setWindowIcon(QIcon("lukeicon.png"))
        self.resize(1024,1024)
        self.startGame()

    def startGame(self):
        self.gameWindow = view()
        self.gameWindow.resize(1024,1024)
        self.setCentralWidget(self.gameWindow)

def main():
    app = QApplication(sys.argv)
    w = mainWindow()
    w.show()

    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
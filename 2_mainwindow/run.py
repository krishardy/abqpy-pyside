import sys

from PySide import QtGui

class MainWindow(QtGui.QMainWindow):
    def __init__(self):
        """
        Initialize the main window
        """
        super(MainWindow, self).__init__()
        self.setWindowTitle("2: MainWindow")

        centralWidget = QtGui.QWidget(self)

        # Create 3 buttons
        start_button = QtGui.QPushButton("Start", self)
        stop_button = QtGui.QPushButton("Stop", self)
        quit_button = QtGui.QPushButton("Quit", self)

        # Lay them out horizontally
        layout = QtGui.QHBoxLayout(self)
        layout.addWidget(start_button)
        layout.addWidget(stop_button)
        layout.addWidget(quit_button)
        centralWidget.setLayout(layout)

        self.setCentralWidget(centralWidget)

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    app.exec_()  # This starts the event loop

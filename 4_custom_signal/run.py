import sys

from PySide import QtGui, QtCore

class MainWindow(QtGui.QMainWindow):
    #: Use this signal to update the status bar message
    updateStatusBar = QtCore.Signal(str)

    def __init__(self):
        """
        Initialize the main window
        """
        super(MainWindow, self).__init__()
        self.setWindowTitle("2: MainWindow")

        centralWidget = QtGui.QWidget(self)

        # Create 3 buttons
        start_button = QtGui.QPushButton("Start", self)
        start_button.clicked.connect(self.on_start_click)

        stop_button = QtGui.QPushButton("Stop", self)
        stop_button.clicked.connect(self.on_stop_click)

        quit_button = QtGui.QPushButton("Quit", self)
        quit_button.clicked.connect(self.close)
        # Clicked signal causes close signal to be emitted, which is handled
        # by self.closeEvent slot.

        # Lay them out horizontally
        layout = QtGui.QHBoxLayout(centralWidget)
        layout.addWidget(start_button)
        layout.addWidget(stop_button)
        layout.addWidget(quit_button)
        centralWidget.setLayout(layout)

        self.setCentralWidget(centralWidget)

        self.statusBar().show()
        # Show the status bar to keep the window from moving stuff around
        # when the statusBar is shown the first time.

        self.updateStatusBar.connect(self.update_status_bar)

    @QtCore.Slot()
    def on_start_click(self):
        self.updateStatusBar.emit("Start clicked")

    @QtCore.Slot()
    def on_stop_click(self):
        self.updateStatusBar.emit("Stop clicked")

    @QtCore.Slot(str)
    def update_status_bar(self, message):
        self.statusBar().showMessage(message)

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    app.exec_()  # This starts the event loop

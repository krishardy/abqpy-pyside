import sys
import logging
import time

from PySide import QtGui, QtCore

logging.basicConfig(level=logging.DEBUG)

class MainWindow(QtGui.QMainWindow):
    #: Use this signal to update the status bar message
    updateStatusBar = QtCore.Signal(str)

    def __init__(self):
        """
        Initialize the main window
        """
        super(MainWindow, self).__init__()
        self.setWindowTitle("2: MainWindow")

        file_menu = self.menuBar().addMenu("&File")
        start_action = file_menu.addAction("&Start")
        start_action.setShortcut("Ctrl+S")
        start_action.triggered.connect(self.on_start_click)

        stop_action = file_menu.addAction("S&top")
        stop_action.setShortcut("Ctrl+T")
        stop_action.triggered.connect(self.on_stop_click)

        file_menu.addSeparator()
        exit_action = file_menu.addAction("&Quit")
        exit_action.setShortcut(QtGui.QKeySequence.Quit)
        exit_action.triggered.connect(self.close)

        help_menu = self.menuBar().addMenu("&Help")
        help_action = help_menu.addAction("&Help")
        help_action.setShortcut(QtGui.QKeySequence.HelpContents)
        help_action.triggered.connect(self.on_help)

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

        self.progress_bar = QtGui.QProgressBar(self)
        # Using self here because I need to reference this in a slot

        # Lay them out horizontally
        button_container = QtGui.QWidget(self)
        button_layout = QtGui.QHBoxLayout(button_container)
        button_layout.addWidget(start_button)
        button_layout.addWidget(stop_button)
        button_layout.addWidget(quit_button)
        button_container.setLayout(button_layout)

        centralLayout = QtGui.QVBoxLayout(centralWidget)
        centralLayout.addWidget(button_container)
        centralLayout.addWidget(self.progress_bar)
        centralWidget.setLayout(centralLayout)

        self.setCentralWidget(centralWidget)

        self.statusBar().show()
        # Show the status bar to keep the window from moving stuff around
        # when the statusBar is shown the first time.

        self.updateStatusBar.connect(self.update_status_bar)

        self.subthread = QtCore.QThread(self)
        self.gregory_leibniz = GregoryLeibniz()
        self.gregory_leibniz.progress.connect(self.on_gl_progress)
        self.gregory_leibniz.done.connect(self.on_gl_done)
        self.subthread.start()
        self.gregory_leibniz.moveToThread(self.subthread)

    @QtCore.Slot()
    def on_start_click(self):
        self.gregory_leibniz.start.emit(5)

    @QtCore.Slot()
    def on_stop_click(self):
        self.updateStatusBar.emit("Stop clicked")

    @QtCore.Slot(str)
    def update_status_bar(self, message):
        self.statusBar().showMessage(message)

    @QtCore.Slot()
    def on_help(self):
        QtGui.QMessageBox.information(self,
                "Help",
                "Press Start to start processing.  Press Stop to stop "
                "processing.  Press Quit to exit the program.",
                QtGui.QMessageBox.Ok,
                QtGui.QMessageBox.Ok)

    @QtCore.Slot(float, str)
    def on_gl_progress(self, value, message):
        self.progress_bar.setValue(value)
        self.updateStatusBar.emit(message)

    @QtCore.Slot(str)
    def on_gl_done(self, value):
        self.progress_bar.setValue(100)
        self.updateStatusBar.emit("pi={}".format(value))

    def closeEvent(self, event):
        self.subthread.quit()
        self.subthread.wait()


class GregoryLeibniz(QtCore.QObject):
    start = QtCore.Signal(int)
    progress = QtCore.Signal(float, str)
    done = QtCore.Signal(float)

    def __init__(self, parent=None):
        super(GregoryLeibniz, self).__init__(parent)
        self.start.connect(self.calculate)

    @QtCore.Slot(int)
    def calculate(self, iterations):
        #logging.debug(QtCore.QThread.currentThreadId())
        #logging.debug(self.currentThread())
        pi = 0.0
        for i in xrange(iterations):
            if i % 2 == 0:
                pi += 4.0 / (2.0 * i + 1.0)
            else:
                pi -= 4.0 / (2.0 * i + 1.0)
            self.progress.emit((float(i) / float(iterations)) * 100.0, "i={0} pi={1}".format(i, pi))
            time.sleep(1)
        self.done.emit(pi)


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    app.exec_()  # This starts the event loop

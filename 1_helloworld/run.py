import sys

from PySide import QtGui

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    widget = QtGui.QWidget()
    widget.setWindowTitle("Hello World")
    widget.show()
    app.exec_()  # This starts the event loop

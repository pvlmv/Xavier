import os
import sys
from PySide6 import QtWidgets, QtGui
from src.app import Window
  
if __name__ == "__main__":
    if getattr(sys, "frozen", False):
        os.chdir(os.path.dirname(sys.executable))

    app = QtWidgets.QApplication([])
    icon = QtGui.QIcon("src/img/icon.ico")
    widget = Window()
    widget.setWindowTitle("Xavier")
    widget.setWindowIcon(icon)
    widget.resize(400, 400)
    widget.show()
    sys.exit(app.exec())
import sys
from PySide6 import QtCore, QtWidgets, QtGui
import document_generator as docG

class Window(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.gitLink = QtWidgets.QLabel('<a href="https://github.com/pvlmv/Xavier"><img src="img/github-icon.png" width="16" height="16"></a>')
        self.text = QtWidgets.QLabel("Welcome to Xavier!", alignment=QtCore.Qt.AlignCenter)
        self.button = QtWidgets.QPushButton("Generate")
        self.gitLink.setOpenExternalLinks(True)

        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(self.gitLink)
        self.layout.addWidget(self.text)
        self.layout.addWidget(self.button)

        self.button.clicked.connect(lambda: docG.generate_docx_with_applied_item('templates/example_template.docx','example_output.docx', docG.get_item_from_yaml('items/example_item.yaml')))
       
if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    
    icon = QtGui.QIcon("img/icon.ico")

    widget = Window()
    widget.setWindowTitle("Xavier")
    widget.setWindowIcon(icon)
    widget.resize(400, 400)
    widget.show()
    
    sys.exit(app.exec())
    

import sys
import yaml
from PySide6 import QtCore, QtWidgets
from document_generator import generate_docx_with_applied_item
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper

with open("items/example_item.yaml", 'r') as f:
    example_item = yaml.load(f, Loader=yaml.FullLoader)
    
print(example_item)

class Window(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.button = QtWidgets.QPushButton("Click to generate new file!")
        self.text = QtWidgets.QLabel("Hello World",
        alignment=QtCore.Qt.AlignCenter)

        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(self.text)
        self.layout.addWidget(self.button)

        self.button.clicked.connect(self.magic)

    @QtCore.Slot()
    def magic(self):
        generate_docx_with_applied_item('templates/example_template.docx','example_output.docx', example_item)
        
if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    widget = Window()
    widget.resize(400, 400)
    widget.show()
    
    sys.exit(app.exec())
    

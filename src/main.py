import sys
from PySide6 import QtCore, QtWidgets, QtGui
import document_generator as docG

EXAMPLE_CHOICES = {
    "claimant" : {'path':'items/Person.csv','id':"Program Author"},
    "respondent" : {'path':'items/Person.csv','id':"John Doe"},
    "amount": "1000",
    "deadline_days": "30"
}

TEMPLATE_PATH = 'templates/example_template.docx'
OUTPUT_PATH = 'example_output.docx'

class Window(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.gitLink = QtWidgets.QLabel('<a href="https://github.com/pvlmv/Xavier"><img src="src/img/github-icon.png" width="16" height="16"></a>')
        self.text = QtWidgets.QLabel("Welcome to Xavier!", alignment=QtCore.Qt.AlignCenter)
        self.button = QtWidgets.QPushButton("Generate")
        self.gitLink.setOpenExternalLinks(True)

        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(self.gitLink)
        self.layout.addWidget(self.text)
        self.layout.addWidget(self.button)

        self.button.clicked.connect(lambda: docG.generate_docx_with_applied_item(TEMPLATE_PATH,OUTPUT_PATH, docG.generate_final_input_item(docG.expect_items_from_docx(TEMPLATE_PATH), EXAMPLE_CHOICES)))
       
if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    
    icon = QtGui.QIcon("src/img/icon.ico")

    widget = Window()
    widget.setWindowTitle("Xavier")
    widget.setWindowIcon(icon)
    widget.resize(400, 400)
    widget.show()
    
    sys.exit(app.exec())
    

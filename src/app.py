import os
import document_generator as docG
from PySide6 import QtCore, QtWidgets

class Window(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QtWidgets.QVBoxLayout(self)
        self.home()

    def home(self):
        self.clear_layout()
        self.gitLink = QtWidgets.QLabel('<a href="https://github.com/pvlmv/Xavier"><img src="src/img/github-icon.png" width="16" height="16"></a>')
        self.gitLink.setOpenExternalLinks(True)
                
        self.text = QtWidgets.QLabel("Welcome to Xavier!", alignment=QtCore.Qt.AlignCenter)
                
        self.button = QtWidgets.QPushButton("Generate")
        self.button.clicked.connect(lambda: self.generator_UI("./templates/"+self.template_drop_down.currentText()+".docx"))
                
        self.template_drop_down = QtWidgets.QComboBox()
        self.template_drop_down.addItems([file.split('.')[0] for file in os.listdir("templates") if file.endswith(".docx")])
        self.layout.addWidget(self.gitLink)
        self.layout.addWidget(self.text)
        self.layout.addWidget(self.template_drop_down)
        self.layout.addWidget(self.button)
        
    def clear_layout(self):
        while self.layout.count():
            child = self.layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
    
    def generator_UI(self, template_path:str):
        
        def get_choices(choices_input:dict[str, QtWidgets.QWidget]) -> dict[str, str | list[str]]:
            choices = dict()
            for name, widget in choices_input.items():
                if isinstance(widget, QtWidgets.QLineEdit):
                    choices[name] = widget.text()
                elif isinstance(widget, QtWidgets.QComboBox):
                    choices[name] = {'path':"./items/"+docG.find_fitting_items(docG.expect_items_from_docx(template_path)[name])[widget.currentText().split(' [')[0]], 'id':widget.currentText().split(' [')[0]}
            return choices
        
        def generate_document_and_leave(choices:dict[str, str], output_path:str = "output.docx"):
            docG.generate_docx_with_applied_item(template_path,"./"+output_path, docG.generate_final_input_item(docG.expect_items_from_docx(template_path), get_choices(choices)))
            self.home()
      
        self.clear_layout()
        
        back_button = QtWidgets.QPushButton("Back")
        back_button.clicked.connect(self.home)
        self.layout.addWidget(back_button)
        
        choices = dict()
        for expected_item_name, expected_item_attributes in docG.expect_items_from_docx(template_path).items():
            if expected_item_name == "UNIT":
                for unit_name in expected_item_attributes:
                    line_edit = QtWidgets.QLineEdit()
                    setattr(self, unit_name+"_line_edit", line_edit)
                    choices[unit_name] = line_edit
                    self.layout.addWidget(QtWidgets.QLabel(f"Enter {unit_name}:"))
                    self.layout.addWidget(line_edit)
                continue
            fitting_items_with_paths = docG.find_fitting_items(expected_item_attributes)
            drop_down = QtWidgets.QComboBox()
            drop_down.addItems([f'{name} [{fitting_items_with_paths[name].split('.')[0]}]' for name in fitting_items_with_paths.keys()])
            setattr(self, expected_item_name+"_drop_down", drop_down)
            choices[expected_item_name] = drop_down
            self.layout.addWidget(QtWidgets.QLabel(f"Choose {expected_item_name}:"))
            self.layout.addWidget(drop_down)
        
        line_edit = QtWidgets.QLineEdit()
        setattr(self, "output_file_name_line_edit", line_edit)
        output_path = line_edit
        self.layout.addWidget(QtWidgets.QLabel(f"Enter Output file name:"))
        self.layout.addWidget(line_edit)
        
        button = QtWidgets.QPushButton("Generate Document")
        button.clicked.connect(lambda: generate_document_and_leave(choices, output_path.text() if output_path.text().endswith(".docx") else output_path.text()+".docx"))
        self.layout.addWidget(button)
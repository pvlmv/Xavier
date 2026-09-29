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
        
        self.gitLink = QtWidgets.QLabel('<a href="https://github.com/pvlmv/Xavier"><img src="src/img/github-icon.png" width="16" height="16"></a>', openExternalLinks=True)
        self.layout.addWidget(self.gitLink)
        
        self.add_button("Settings",self.settings_UI)
        
        self.add_button("Open Work Directory", self.open_directory)
                
        self.text = QtWidgets.QLabel("Welcome to Xavier!", alignment=QtCore.Qt.AlignCenter)
        self.layout.addWidget(self.text)
        
        self.add_labeled_drop_down("template", [file.split('.')[0] for file in os.listdir("templates") if file.endswith(".docx")])
        
        self.add_button("Generate", lambda: self.generator_UI("./templates/"+self.template_drop_down.currentText()+".docx"))
    
    def open_directory(self):
        try:
            absolute_path = os.path.abspath(".")
            os.startfile(absolute_path, "open")
        except:
            QtWidgets.QMessageBox.warning(self, "Warning", f"Failed to open work directory")
        
    def clear_layout(self):
        while self.layout.count():
            child = self.layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
                
    def add_button(self,text:str,callback:callable) -> QtWidgets.QPushButton:
        button = QtWidgets.QPushButton(text)
        button.clicked.connect(callback)
        self.layout.addWidget(button)
        return button
    
    def add_labeled_check_box(self,content_name:str,default_value:bool=False) -> QtWidgets.QCheckBox:
        check_box = QtWidgets.QCheckBox()
        setattr(self,content_name+"_check_box",check_box)
        self.layout.addWidget(QtWidgets.QLabel(content_name+":"))
        self.layout.addWidget(check_box)
        check_box.setCheckState(QtCore.Qt.Checked if default_value else QtCore.Qt.Unchecked)
        return check_box
                
    def add_labeled_line_edit(self,content_name:str,default_value:str = "") -> QtWidgets.QLineEdit:
        line_edit = QtWidgets.QLineEdit()
        setattr(self, content_name+"_line_edit", line_edit)
        self.layout.addWidget(QtWidgets.QLabel("Enter "+content_name+":"))
        self.layout.addWidget(line_edit)
        line_edit.setText(default_value)
        return line_edit
            
    def add_labeled_drop_down(self,content_name:str,items:list[str]) -> QtWidgets.QComboBox:
        drop_down = QtWidgets.QComboBox()
        drop_down.addItems(items)
        setattr(self, content_name+"_drop_down", drop_down)
        self.layout.addWidget(QtWidgets.QLabel("Choose "+content_name+":"))
        self.layout.addWidget(drop_down)
        return drop_down
    
    def settings_UI(self):
        def saveChanges(default_date_format:str,open_file_after_generation:QtCore.Qt.CheckState):
            open_file_after_generation_bool : bool = True if open_file_after_generation == QtCore.Qt.Checked else False
            with open("./config.txt","w") as f:
                f.write("default_date_format "+default_date_format+"\n")
                f.write("open_file_after_generation "+str(open_file_after_generation_bool).lower()+"\n")
            self.home()
        
        default_date_format = "%d.%m.%Y"
        open_file_after_generation = False
        try:
            with open("./config.txt") as f:
                settings : dict[str,str] = {line.split(' ')[0]:line.split(' ')[1].strip() for line in f.readlines()}
                open_file_after_generation = settings["open_file_after_generation"].lower() == "true"
                default_date_format = settings["default_date_format"]
        except:None
        
            
        self.clear_layout()
        self.add_button("Back",self.home)
        self.add_labeled_line_edit("default_date_format",default_date_format)
        self.add_labeled_check_box("open_file_after_generation",open_file_after_generation)
        self.add_button("Submit changes",lambda: saveChanges(self.default_date_format_line_edit.text(), self.open_file_after_generation_check_box.checkState()))
    
    def generator_UI(self, template_path:str):
        def add_variable_menu_from_template(window:Window, template_path:str) -> dict[str,str]:
            choices = dict()
            expected_items :dict[str,list[str] | str] = docG.expect_items_from_docx(template_path)
            unit_variables = expected_items.pop("UNIT") if len(expected_items.get("UNIT")) != 0 else []
            for expected_item_name, expected_item_attributes in expected_items.items():
                fitting_items_with_paths = docG.find_fitting_items(expected_item_attributes)
                choices[expected_item_name] = window.add_labeled_drop_down(expected_item_name, [f'{name} [{fitting_items_with_paths[name].split('.')[0]}]' for name in fitting_items_with_paths.keys()])
            for unit_name in unit_variables:
                if not docG.PRESET_VARIABLES.__contains__(unit_name): choices[unit_name] = window.add_labeled_line_edit(unit_name)
            return choices
        
        def extract_paths_and_names_from_QtWidgets(choices_input:dict[str, QtWidgets.QWidget]) -> dict[str, str | list[str]]:
            choices = dict()
            for name, widget in choices_input.items():
                if isinstance(widget, QtWidgets.QLineEdit):
                    choices[name] = widget.text()
                elif isinstance(widget, QtWidgets.QComboBox):
                    choices[name] = {'path':"./items/"+docG.find_fitting_items(docG.expect_items_from_docx(template_path)[name])[widget.currentText().split(' [')[0]], 'id':widget.currentText().split(' [')[0]}
            return choices
        
        def generate_document_and_return_home(choices:dict[str, str], output_path:str = "output.docx"):
            final_input_item = docG.generate_final_input_item(docG.expect_items_from_docx(template_path), extract_paths_and_names_from_QtWidgets(choices))
            docG.generate_docx_with_applied_item(template_path,"./"+output_path, final_input_item)
            self.home()
      
        def validate_and_generate(choices:dict[str, str], output_path:str = "output.docx"):
            for name, value in extract_paths_and_names_from_QtWidgets(choices).items():
                value = value.strip() if isinstance(value, str) else value
                if value == "" or value == {'path':"./items/", 'id':""}:
                    QtWidgets.QMessageBox.warning(self, "Warning", f"Please fill in all fields. Missing: {name}")
                    return
            generate_document_and_return_home(choices, output_path)
  
        self.clear_layout()
        self.add_button("Back",self.home)
        choices = add_variable_menu_from_template(self, template_path)
        output_path = self.add_labeled_line_edit("Output_File", template_path.split('/')[-1].split('.')[0]+".docx")
        self.add_button("Generate Document",lambda: validate_and_generate(choices, output_path.text() if output_path.text().endswith(".docx") else output_path.text()+".docx"))
import os
from src import logic as docG
from PySide6 import QtCore, QtWidgets

class Window(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setObjectName("xavierWindow")
        self.setMinimumSize(320, 400)
        self.setMaximumSize(800, 800)
        self.setStyleSheet("""
            QWidget#xavierWindow {
                background-color: #f3f5f9;
                color: #202b3c;
                font-family: "Segoe UI";
                font-size: 10pt;
            }
            QLabel {
                color: #344256;
                font-weight: 500;
            }
            QLabel#welcomeTitle {
                color: #172b4d;
                font-size: 20pt;
                font-weight: 700;
                padding: 12px 0;
            }
            QLabel#githubLink {
                padding: 2px 0;
            }
            QPushButton {
                color: #ffffff;
                background-color: #315fca;
                border: none;
                border-radius: 8px;
                min-height: 38px;
                padding: 0 16px;
                font-weight: 600;
            }
            QPushButton:hover {
                background-color: #244fae;
            }
            QPushButton:pressed {
                background-color: #1d418f;
            }
            QLineEdit, QComboBox {
                background-color: #ffffff;
                color: #202b3c;
                border: 1px solid #cbd4e1;
                border-radius: 7px;
                min-height: 36px;
                padding: 0 10px;
                selection-background-color: #315fca;
            }
            QLineEdit:focus, QComboBox:focus {
                border: 2px solid #5882df;
            }
            QComboBox::drop-down {
                border: none;
                width: 28px;
            }
            QComboBox QAbstractItemView {
                background-color: #ffffff;
                color: #202b3c;
                border: 1px solid #cbd4e1;
                outline: none;
                font-size: 10pt;
                selection-background-color: #315fca;
                selection-color: #ffffff;
            }
            QComboBox QAbstractItemView::item {
                min-height: 30px;
                padding: 4px 10px;
            }
            QComboBox QAbstractItemView::item:hover {
                background-color: #e8eefb;
                color: #202b3c;
            }
            QComboBox QAbstractItemView::item:selected {
                background-color: #315fca;
                color: #ffffff;
            }
            QCheckBox {
                spacing: 8px;
                padding: 4px 0;
            }
            QCheckBox::indicator {
                width: 18px;
                height: 18px;
                background-color: #ffffff;
                border: 1px solid #738198;
                border-radius: 4px;
            }
            QCheckBox::indicator:hover {
                background-color: #e8eefb;
                border: 1px solid #315fca;
            }
            QCheckBox::indicator:checked {
                background-color: #315fca;
                border: 1px solid #244fae;
            }
            QCheckBox::indicator:checked:hover {
                background-color: #244fae;
            }
            QCheckBox::indicator:disabled {
                background-color: #e5e9f0;
                border: 1px solid #b6bfcd;
            }
        """)
        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.setContentsMargins(28, 24, 28, 24)
        self.layout.setSpacing(14)
        self.home()

    def changeEvent(self, event: QtCore.QEvent) -> None:
        if event.type() == QtCore.QEvent.Type.WindowStateChange and self.isFullScreen():
            self.showNormal()
        super().changeEvent(event)

    def home(self):
        self.clear_layout()
        actions_layout = QtWidgets.QHBoxLayout()
        actions_layout.setSpacing(10)
        self.layout.addLayout(actions_layout)

        self.gitLink = QtWidgets.QLabel('<a href="https://github.com/pvlmv/Xavier"><img src="src/img/github-icon.png" width="16" height="16"></a>', openExternalLinks=True)
        self.gitLink.setObjectName("githubLink")
        actions_layout.addWidget(self.gitLink)
        
        self.add_button("Settings", self.settings_UI, actions_layout)
        
        self.add_button("Open Work Directory", self.open_directory, actions_layout)
                
        self.text = QtWidgets.QLabel("Welcome to Xavier!", alignment=QtCore.Qt.AlignCenter)
        self.text.setObjectName("welcomeTitle")
        self.layout.addWidget(self.text)
        
        self.add_labeled_drop_down("template", [file.split('.')[0] for file in os.listdir("contents/templates") if file.endswith(".docx")])
        
        self.add_button("Generate", lambda: self.generator_UI("./contents/templates/"+self.template_drop_down.currentText()+".docx"))
    
    def open_directory(self):
        try:
            absolute_path = os.path.abspath(".")
            os.startfile(absolute_path, "open")
        except:
            QtWidgets.QMessageBox.warning(self, "Warning", f"Failed to open work directory")
        
    def clear_layout(self):
        def clear_nested_layout(layout: QtWidgets.QLayout) -> None:
            while layout.count():
                item = layout.takeAt(0)
                nested_layout = item.layout()
                if nested_layout is not None:
                    clear_nested_layout(nested_layout)
                    nested_layout.deleteLater()
                elif item.widget() is not None:
                    item.widget().deleteLater()

        clear_nested_layout(self.layout)
                
    def add_button(self,text:str,callback:callable,layout:QtWidgets.QBoxLayout|None=None) -> QtWidgets.QPushButton:
        button = QtWidgets.QPushButton(text)
        button.clicked.connect(callback)
        target_layout = layout if layout is not None else self.layout
        target_layout.addWidget(button)
        return button

    def add_labeled_input_row(self, label_text: str, widget: QtWidgets.QWidget) -> None:
        row = QtWidgets.QWidget()
        row_layout = QtWidgets.QHBoxLayout(row)
        row_layout.setContentsMargins(0, 0, 0, 0)
        #row_layout.setSpacing(2)
        label = QtWidgets.QLabel(label_text)
        label.setMinimumWidth(90)
        row_layout.addWidget(label)
        row_layout.addWidget(widget, 1)
        self.layout.addWidget(row)
    
    def add_labeled_check_box(self,content_name:str,default_value:bool=False) -> QtWidgets.QCheckBox:
        check_box = QtWidgets.QCheckBox()
        setattr(self,content_name+"_check_box",check_box)
        row = QtWidgets.QWidget()
        row_layout = QtWidgets.QHBoxLayout(row)
        row_layout.setContentsMargins(0, 0, 0, 0)
        row_layout.setSpacing(12)
        label = QtWidgets.QLabel(content_name+":")
        label.setMinimumWidth(180)
        row_layout.addWidget(label)
        row_layout.addWidget(check_box, 1)
        self.layout.addWidget(row)
        check_box.setCheckState(QtCore.Qt.Checked if default_value else QtCore.Qt.Unchecked)
        return check_box
                
    def add_labeled_line_edit(self,content_name:str,default_value:str = "") -> QtWidgets.QLineEdit:
        line_edit = QtWidgets.QLineEdit()
        setattr(self, content_name+"_line_edit", line_edit)
        self.add_labeled_input_row("Enter "+content_name+":", line_edit)
        line_edit.setText(default_value)
        return line_edit
            
    def add_labeled_drop_down(self,content_name:str,items:list[str]) -> QtWidgets.QComboBox:
        drop_down = QtWidgets.QComboBox()
        drop_down.addItems(items)
        setattr(self, content_name+"_drop_down", drop_down)
        self.add_labeled_input_row("Choose "+content_name+":", drop_down)
        return drop_down
    
    def settings_UI(self):
        def saveChanges(default_date_format:str,open_file_after_generation:QtCore.Qt.CheckState):
            open_file_after_generation_bool : bool = True if open_file_after_generation == QtCore.Qt.Checked else False
            with open("./contents/config.txt","w") as f:
                f.write("default_date_format "+default_date_format+"\n")
                f.write("open_file_after_generation "+str(open_file_after_generation_bool).lower()+"\n")
            self.home()
        
        default_date_format = "%d.%m.%Y"
        open_file_after_generation = False
        try:
            with open("./contents/config.txt") as f:
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
                    choices[name] = {'path':"./contents/items/"+docG.find_fitting_items(docG.expect_items_from_docx(template_path)[name])[widget.currentText().split(' [')[0]], 'id':widget.currentText().split(' [')[0]}
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
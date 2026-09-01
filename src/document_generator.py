import re
import os
import yaml
from docx import Document
from PySide6.QtCore import Slot

@Slot()
def generate_docx_with_applied_item(template_path: str, output_path: str, item):
    Document(template_path).save(output_path)
    document = Document(output_path)
    
    for paragraph in document.paragraphs:
        for variable, value in item.items():
            paragraph.text = re.sub(rf'\$\`{variable}\`', value, paragraph.text)
    document.save(output_path)
    # os.system(f"start {output_path}") Open generated document

@Slot()
def get_item_from_yaml(yaml_path: str):
    with open(yaml_path, 'r') as f:
        example_item = yaml.load(f, Loader=yaml.FullLoader)
    return example_item

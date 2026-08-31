from docx import Document
import re

def generate_docx_with_applied_item(template_path: str, output_path: str, item):
    Document(template_path).save(output_path)
    document = Document(output_path)

    for paragraph in document.paragraphs:
        for variable, value in item.items():
            paragraph.text = re.sub(rf'\$\`{variable}\`', value, paragraph.text)
    document.save(output_path)
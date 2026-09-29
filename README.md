# Xavier - DOCX templater

Xavier is an open-source DOCX templating application. It generates documents
from Word templates and user-defined CSV content.

## User guide

### Generate a document

1. Select a template and choose **Generate**.
2. Choose an item for each requested item type and enter values for the
   requested unit placeholders.
3. Set the output file name and choose **Generate Document**.

The generated document is saved in `contents/`. Xavier opens it automatically
when **Open file after generation** is enabled in Settings. The `contents/items`
and `contents/templates` folders include sample data and a sample template.

### Create a template

Create a `.docx` file and replace the text to be filled in with placeholders.
Save the template in `contents/templates`.

Placeholders start with `$` and are enclosed in grave accents. Use letters,
digits, and underscores in names, with no spaces. Xavier supports:

- **Item placeholders**, in the form `item_name.attribute_name`. Xavier fills
  these from a matching CSV item. For example: ``$`claimant.first_name` ``.
- **Unit placeholders**, which users fill in during document generation.
  They can be written as ``$`UNIT.amount` ``, ``$`amount` ``, or
  ``$`.postal_code` ``.

Examples of invalid placeholders include `$amount` (missing grave accents),
``$`claimant's.name` `` (apostrophe), and ``$`postal code` `` (space).
See `contents/templates/example_template.docx` for a working example.

### Create CSV content

Create a `.csv` file in `contents/items`. The file name identifies its item
type. Put the column names in the first row, including a unique `id` column
and every attribute used by the corresponding template. Add one item per
subsequent row. The `id` value identifies each item and must be unique within
the file.

### Current date placeholder

Use ``$`current_date_formatted` `` to insert the current date using the default
format configured in Settings. To specify a format in the template, add it in
parentheses; for example, ``$`current_date_formatted(%d.%m.%Y)` ``. Xavier uses
Python's `strftime` format codes; see the
[Python datetime documentation](https://docs.python.org/3/library/datetime.html#strftime-strptime-behavior).

## License

This project is licensed under the MIT License.

Copyright 2026 Tymon Raciński

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the “Software”), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

## Windows distribution

A prebuilt executable is available from the
[windows-download branch](https://github.com/pvlmv/Xavier/blob/windows-download/Xavier.zip).

To build the application on Windows, run these commands from the project root:

```powershell
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m pip install pyinstaller
.\.venv\Scripts\pyinstaller.exe --noconfirm --clean --onedir --windowed --name Xavier --icon src\img\icon.ico --contents-directory . --paths . --add-data "contents;contents" --add-data "src\img;src\img" src\main.py
```

The build creates `dist\Xavier`. Distribute the entire folder, including
`Xavier.exe` and `contents`. Users can add or edit templates and CSV files in
`contents`; Xavier also saves settings and generated documents there. Install
the distribution in a location where users have write permission.

Build on Windows for the same architecture as the target PCs. PyInstaller does
not cross-compile Windows executables from other operating systems.

## Feedback

For questions or feedback, contact the author on
[LinkedIn](https://www.linkedin.com/in/tymon-racinski-667bb6372/).
If you find Xavier helpful please post about it and tag me. **Thank you.**

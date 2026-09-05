
# TODO

- Document generation
- Encoding error fix
- Dynamic date formating
- Test 'UNIT.' variable names
- Setting for opening the generated document automatically/opening directory/doing nothing
- Clean UI
- Create .exe version
- Create macOS version

## Potential future features

- Check for updates on github

## Details

A template is a .docx file containing Variables (like such: \$\`Item_name.variable_name\` or simply \$\`unit_variable_name\`). Before loading Item data into a template the program shall check what ItemTypes are suitable based on the required attributes and will only suggest Items of those ItemTypes. Program will open text input windows to ammend UnitVariable values of the template.

---
To generate a document choose a template, choose corresponding Items from a dropdown list and fill the UnitVariable text boxes.

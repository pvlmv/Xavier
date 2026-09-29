# Xavier

An easy to use docx templater with loadable customisable content.

## Windows distribution

Build on Windows from the project root with the project environment activated:

```powershell
.\Scripts\pyinstaller.exe --noconfirm --clean Xavier.spec
```

The build creates a windowed, one-folder distribution at `dist\Xavier`. Distribute
the entire folder; users can start `Xavier.exe`. The editable `contents` folder
(templates, item CSVs, and settings) is placed beside the executable so users can
add or modify content. Keep the distribution in a folder where users have write
permissions, since settings and generated documents are saved there.

Build with the same architecture as the target Windows PCs. PyInstaller does not
cross-compile Windows executables from other operating systems.

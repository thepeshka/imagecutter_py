from cx_Freeze import setup, Executable
import os
os.environ['TCL_LIBRARY'] = r'C:\\Users\\peshka\\AppData\\Local\\Programs\\Python\\Python36-32\\tcl\\tcl8.6'
os.environ['TK_LIBRARY'] = r'C:\\Users\\peshka\\AppData\\Local\\Programs\\Python\\Python36-32\\tcl\\tk8.6'

base = None    

executables = [Executable("main.py", base=base)]

packages = ["idna"]
options = {
    'build_exe': {    
        'packages':packages,
        'include_files': ["tcl86t.dll", "tk86t.dll"]
    },    
}

setup(
    name = "imagecutter_py",
    options = options,
    version = "0.0.0.1",
    description = 'imagecutter',
    executables = executables
)

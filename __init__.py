from startup_utils import Python
from UI import UI
from pathlib import Path
import subprocess
import os


answer = UI.confirming("Check for imports and install it? Warning! Long process!", "start")
if answer == True:
    Python.installing_depends(Python.searching(Path.cwd(), "modules"))
else:
    subprocess.run((f"python{Python.get_python_version()}", "gibot.py"))
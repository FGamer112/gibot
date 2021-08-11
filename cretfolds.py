import os
path = os.path.dirname(__file__)
input_colichestvo = int(input("Number of folders: "))
colichestvo = range(1, input_colichestvo+1, 1)
name = str
input_name = str(input("Name of folder: "))
for i in colichestvo:
    name = str(i)
    os.system(f"cd {path} && mkdir {input_name}{name}")

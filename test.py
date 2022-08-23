import subprocess
from time import sleep
def printing(count:int, delay: int):
    i = 1
    while i<=count:
        print(f"working{i}")
        sleep(delay)
        i+=1
subprocess.Popen(printing(10, 0.1)).wait()
subprocess.Popen(printing(10, 0.5)).wait()
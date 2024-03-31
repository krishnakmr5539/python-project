import os 
import shutil
import tarfile
import sys
import time

today_date = time.strftime("%Y-%m%d") #time in 2024-0326 formate
year = time.strftime("%Y")
# path of the directory 
master_dir = "/volume/CSdata/krikumar/Microsoft"

dir_path = "/volume/CSdata/krikumar/Microsoft/" + today_date

print(today_date)
# Getting the list of directories 
dir = os.listdir(dir_path) 

print(dir)

for d in range(len(dir)):
    print(d)


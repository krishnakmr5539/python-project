import os 
import shutil
import tarfile
import sys
import time
import datetime


today_date = time.strftime("%Y-%m%d") #time in 2024-0326 formate
year = time.strftime("%Y")

# path of the directory 
master_dir = "/volume/CSdata/krikumar/test-dir"

# dir_path = "/volume/CSdata/krikumar/Microsoft/" + today_date

# print("Todays date:",today_date)
# Getting the list of directories 
dir = os.listdir(master_dir) 

# print(dir)

for d in dir:
    print("Directory is :",d)
    d1=d

    dir_1 = "/volume/CSdata/krikumar/test-dir/" + d1
    os.chdir(dir_1) 
    path = dir_1 
    modified_time = os.path.getmtime(path)
    modified_date = datetime.datetime.fromtimestamp(modified_time)
    print("modified_time:",modified_date)
    os.system('ls -l')




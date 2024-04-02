import os 
import shutil
import tarfile
import sys
# import time
import datetime

# today_date = time.strftime("%Y-%m%d") #time in 2024-0326 formate
# year = time.strftime("%Y")

# path of the directory 
master_dir = "/volume/CSdata/krikumar/Microsoft"

# dir_path = "/volume/CSdata/krikumar/Microsoft/" + today_date

# print("Todays date:",today_date)
# Getting the list of directories 
dir = os.listdir(master_dir) 

print(dir)

for d in dir:
    print("Directory is :",d)
    d1=d
    print("d1:",d1)
    os.chdir("/volume/CSdata/krikumar/Microsoft/" + d1) 
    # path=  "test"
    create_time = os.path.getctime("test")
    create_date = datetime.datetime.fromtimestamp(create_time)
    print("create_time:",create_date)

# 
# os.system('ls -l')


import os
import shutil
import tarfile
import sys
from datetime import date


os.system('echo ~ > home_dir.txt')
home_dir = open("home_dir.txt", "r") 
txt = home_dir.read()

data_into_list = txt.replace('\n', '', ).split("/") 
del data_into_list[0]

user_name = data_into_list[1]
print("\n\033[94mUser :  {} \n".format(user_name))
home_dir.close() 


case_num1 = input("\033[93mEnter the case number:")
case_num = case_num1.replace(" ","")
get_year = case_num.split('-')
Year = get_year[0]

print("\n")

case_vol = "/volume/case_"+Year+"/" + case_num


print("case_vol dir:",case_vol,"\n")

if(os.path.exists(case_vol)):
    print("Case_volum directory check pass: \n")
else:
    print("\033[91m DIRECTORY {} DOES NOT EXIST".format(case_vol),"\n")
    print("\033[91m Either customer has not yet uploaded logs or logs not synced to case_volume\n")
    print("\033[91m Exiting from the script\n \033[91m")
    print("\033[0m")

    sys.exit(0)


# Check if user has home directory in Csdata #

user_CSdata_dir = "/volume/CSdata/" + user_name

if(os.path.exists(user_CSdata_dir)):
    print("User Csdata home directory check pass: \n")
else:
    print("\033[91m Home Direcroty does not exist in Csdata.Get home directory created by IT team")
    sys.exit(0)


CSdata_dir = "/volume/CSdata/" + user_name+"/"+case_num +"/"


print("Creating CSdata directory:",CSdata_dir,"\n")
try:
   os.mkdir(CSdata_dir)

except FileExistsError:
   print("\033[94m Directory {} already exist, copying file now. ".format(CSdata_dir))


#cwd = os.getcwd() 
#print("Current working directory:\n\n", cwd) 

os.chdir(case_vol) 

cwd = os.getcwd() 
#print("Current working directory:", cwd) 



# Iterate through all file 

for file in os.listdir():

    if "core-tarball" in file:
        file_path = f"{case_vol}/{file}"
        print("Copying core file:",file_path,"\n")
        shutil.copy(file_path,CSdata_dir)

    elif ".core."  in file:
        file_path = f"{case_vol}/{file}"   
        shutil.copy(file_path,CSdata_dir)
        print("Copying core file:",file_path,"\n")
       
    elif file.endswith(".tgz"):  ## Check if file extention is .tgz then extract to CSdata ##

        file_path = f"{case_vol}/{file}"
        file_name = file
        name = os.path.splitext(file_name)
        path = os.path.join(CSdata_dir,name[0])

        try:
            os.mkdir(path)                                 
            print("Extracting File:",file_name,"\n") #print(name[0])  --> 2024-0226-085419-iad39-j1-vpn1-logs#

            try:
                file = tarfile.open(file_path)
                file.extractall(path)         # extracting file 
                file.close()
            except tarfile.ReadError:
                print("\033[91m Not  able to open file:\033[94m", file_path)
               
        except FileExistsError:
                print("\033[94m Directory {} already exist".format(path),"\n")
    else:       
        file_path = f"{case_vol}/{file}"
        print("Copying file to Csdata: {} ".format(file),"\n")
        shutil.copy(file_path,CSdata_dir)
      


os.chdir(CSdata_dir) 
os.system('chmod -R 777 *')

print("\033[92mAll file now in:", CSdata_dir,"\n" )

print("Thank You\n" )
print("\033[0m")

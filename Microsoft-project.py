import os 
import shutil
import tarfile
import time

# os.system('rm -rf /volume/CSdata/krikumar/Microsoft-automation/case-reported-in-last-10-min.txt') #removing last 10th minute case file#
today_date = time.strftime("%Y-%m%d") #time in 2024-0326 formate
year = time.strftime("%Y")
master_dir = "/volume/CSdata/krikumar/Microsoft" # Directory  where cases will be stored#
# dir_path = "/volume/CSdata/krikumar/Microsoft/" + today_date
# dir = os.listdir(master_dir)  # Getting the list of directories 
# if len(dir) == 0:
#     print("creating new dir",dir_path)
#     os.mkdir(dir_path)
# else: 
#     for d in dir:
#         print("Directory in master dir:",d)
#         if d == today_date:
#             print("Directory Exist:",dir_path)
#         else:
#             print("creating dir:",dir_path)
#             os.chdir(master_dir) 
#             os.system('rm -rf *')
#             os.mkdir(dir_path)

# os.system('chmod -R 777 /volume/CSdata/krikumar/Microsoft/*')  

#get case number #
case_file_loc = "/volume/CSdata/krikumar/Microsoft-automation"
os.chdir(case_file_loc)            

file_path1 = 'final-case-list.txt'  # microsoft_case.txt has case number reported in last 10 minutes

# Open the file in read mode
with open(file_path1, 'r') as file: # Read all lines from the file and store them in a list
    lines = file.readlines() # Now, 'lines' contains a list of lines from the file

res = [] #replacing \n with ""#
for sub in lines:
    res.append(sub.replace("\n", ""))
    print("Microsoft case :",sub) 


for x in range(len(res)):
    case_num=(res[x])
    print("case number is",case_num,"\n")
    #apply logic to check if dir already exist #
    case_dir = "/volume/CSdata/krikumar/Microsoft/" + case_num
    if(os.path.exists(case_dir)):
        print("Case directory already exist,no need to extract the logs: \n")       
    else:
        print("Extracting logs to the ",case_dir)
        case_list = []
        case_list.append(case_num) #store the latest case in this list#
        os.mkdir(case_dir) 
        print ("Case Directory is :",case_dir,"\n")
        case_vol = "/volume/case_" + year +"/" + case_num
        os.chdir(case_vol) 
        for file in os.listdir():    # Iterate through all file 
            if "core-tarball" in file:
                file_path = f"{case_vol}/{file}"
                print("Copying core file:",file_path,"\n")
                shutil.copy(file_path,case_dir)
            elif ".core."  in file:
                file_path = f"{case_vol}/{file}"   
                shutil.copy(file_path,case_dir)
                print("Copying core file:",file_path,"\n")      
            elif file.endswith(".tgz"):  ## Check if file extention is .tgz then extract to CSdata ##
                file_path = f"{case_vol}/{file}"
                file_name = file
                name = os.path.splitext(file_name)
                path = os.path.join(case_dir,name[0])
                try:
                    os.mkdir(path)                                 
                    print("Extracting File:",file_name,"\n") #print(name[0])  --> 2024-0226-085419-iad39-j1-vpn1-logs#
                    try:
                        file = tarfile.open(file_path)
                        file.extractall(path)         # extracting file 
                        file.close()
                    except tarfile.ReadError:
                        print("Not  able to open file:", file_path)
                except FileExistsError:
                    print("Directory {} already exist".format(path),"\n")
            else:       
                file_path = f"{case_vol}/{file}"
                print("Copying file to Csdata: {} ".format(file),"\n")
                shutil.copy(file_path,case_dir)
os.chdir(case_dir) 
os.system('chmod -R 777 *')

time.sleep(5)




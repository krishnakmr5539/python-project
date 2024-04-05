
#The Function find the PR from the master list on the basis of the RSI version#

def find_string_in_file(file_path, search_string):
    with open(file_path, 'r') as file:
        for line in file:
            if search_string in line:
                print(line)

# Example usage:
file_path = '/volume/CSdata/krikumar/Microsoft-automation/Final-PR-Report-html-tag-x.html'
search_string = '20.3X75-D34'

find_string_in_file(file_path, search_string)
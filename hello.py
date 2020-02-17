#!/bin/env python
import os
import subprocess

def get_file_name(raw_line):
    name = raw_line[6:len(raw_line)-1]
    return name;

def get_line_numbers(raw_line):
    #Remove the first half junk
    raw_line = raw_line.split("+",1)[1]
    #Remove the second half junk
    raw_line = raw_line.split(" ",1)[0]
    return raw_line.split(",",1)[0], raw_line.split(",",1)[1]
    
def find_diff():
    #Hard code the directory temp
    path="~/opensource/git-hooks"
    os.chdir(path)
    #print(os.getcwd())
    
    bashCommand = "git diff --cached --no-color"
    process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()
    #print(output)
    
    output_file = 'output.magic'
    
    # Writing to a file 
    file1 = open(output_file, 'w') 
    file1.writelines(output)
    file1.close()
    
    # Using readlines() 
    file1 = open(output_file, 'r') 
    lines = file1.readlines() 
    
    #[[file_name, line_number, offset], [file_name, line_number, offset], ...]
    my_list = []
    file_name = ""
    found_file = 0
    
    for line in lines:
        
        #Detect if it is a new file
        if line[0:3] == "+++":
            file_name = get_file_name(line)
            found_file = 1
          
        #Detect if this is the diff of next file 
        if line[0:3] == "---":
                found_file = 0
          
        if found_file == 1 and line[0:2] == "@@":
            line_number, offset = get_line_numbers(line)
            my_list.append([file_name, line_number, offset])
          
    
    print(my_list)
    
    os.remove(output_file)
    return my_list


def fix_tabs(info):
    
    replaced_lines = 0
    
    with open(info[0], 'r') as file0:
        data = file0.readlines()
    
    #print data
    
    #Line numbers of diff start from 1, while python's start from 0
    start = int(info[1]) - 1
    end   = int(info[1]) + int(info [2]) - 1
    
    for l in range(start, end):
        print(data[l])
        replaced = data[l].replace("\t", "    ")
        print(replaced)
        if data[l] != replaced:
            data[l]=replaced
            replaced_lines = replaced_lines + 1
    
    with open(info[0], 'w') as file0:
        file0.writelines(data)
    
    return replaced_lines


def main():
    #Local variables
    replaced_lines = 0
    
    my_list = find_diff()
    
    for info in my_list:
        print(info)
        n = fix_tabs(info)
        replaced_lines = replaced_lines + n
    
    if replaced_lines > 0:
        print(replaced_lines, " Line(s) replaced tabs with spaces")
        print("Aborted.")
        print("Please restage files and try again!")
        return -1
    else:
        return 0
    
    

main()

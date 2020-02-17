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
    return int(raw_line.split(",",1)[0]), int(raw_line.split(",",1)[1])


def fix_broken_diff(output):
        #Fix broken diff lines @@ x,y x,y @@
    found_start = 0
    for element in range(0, len(output)):

        #Ending sequence detector
        if found_start == 1 and output[element:element+2] == "@@":
            #Check what is the next character after ending @@
            if output[element+2] != "\n":
                print("found errorenous diff output")
                output = output[:element+2] + '\n' + output[element+2:]

            found_start = 0
            continue
        
        #Starting sequence detector
        if output[element:element+2] == "@@":
            found_start = 1
            
    return output
    
    
#Merge line numbers of the same files if any
def consoldate_list(list0):
    #list0 = [[name, [10, 15]], ...]
    length = len(list0)
    i = 0
    
    while i < (length - 1):
        a = list0[i]
        b = list0[i+1]
        if a[0] == b[0]:
            for element in b[1]:
                a[1].append(element)
            list0.remove(b)
            length = length - 1
        else:
            i = i + 1
        

def find_diff():
    #Local variables
    status = 0
    output_file = 'output.magic'
    
    #Hard code the directory temp
    #path="/var/mentor/opensource/git-hooks"
    #os.chdir(path)
    
    bashCommand = "git diff --cached"
    process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
    output = process.communicate()
    output = output[0]
      
    # If we have received diff
    if output:
        
        #output = fix_broken_diff(output)
           
        # Writing to a file 
        file1 = open(output_file, 'w') 
        file1.writelines(output)
        file1.close()
        
        # Using readlines() 
        file1 = open(output_file, 'r') 
        lines = file1.readlines() 
        
        #[[file_name, line_number, offset], [file_name, line_number, offset], ...]
        my_list = []
        #[10, 20, 30]
        changed_ln = []
        file_name = ""
        found_file = 0
        found_offsets = 0
        
        for line in lines:
            
            #Detect if it is a new file
            if line[0:3] == "+++":
                file_name = get_file_name(line)
                found_file = 1
              
            #Detect if this is the diff of next file 
            if line[0:3] == "---":
                found_file = 0
              
            if found_file == 1 and line[0:2] == "@@":
                starting_ln, offset = get_line_numbers(line)
                found_offsets = 1
                continue
#                 my_list.append([file_name, starting_ln, offset])
            if found_offsets == 1:
                if line[0] == "+":
                    changed_ln.append(starting_ln)
                    starting_ln = starting_ln + 1
                    offset = offset - 1
                elif line[0] != "-":
                    starting_ln = starting_ln + 1
                    offset = offset - 1
                    
            if found_offsets == 1 and offset == 0:
                my_list.append([file_name, changed_ln])
                changed_ln = []
                found_offsets = 0
                offset = -1
                    
                       
        consoldate_list(my_list)
        
        os.remove(output_file)
        return my_list, status
    else:
        status = -1
        return my_list, status


def fix_tabs(info):
    
    replaced_lines = 0
    
    with open(info[0], 'r') as file0:
        data = file0.readlines()
    
    for l in info[1]:
        #Line numbers of diff start from 1, while python's start from 0
        #print(data[l-1])
        replaced = data[l-1].replace("\t", "    ")
        #print(replaced)
        if data[l-1] != replaced:
            data[l-1] = replaced
            replaced_lines = replaced_lines + 1
    
    with open(info[0], 'w') as file0:
        file0.writelines(data)
    
    return replaced_lines


def main():
    #Local variables
    replaced_lines = 0
    
    my_list, status = find_diff()
    
    print(my_list)
    
    # If status isn't success, return error.
    if status != 0:
        print("No file(s) have been staged.")
        return -1
    
    for info in my_list:
        print(info)
        n = fix_tabs(info)
        replaced_lines = replaced_lines + n
    
    if replaced_lines > 0:
        print(replaced_lines, " Line(s) replaced tabs with spaces")
        print("Aborting...")
        print("Please stage the changed files and try again!")
        return -1
    else:
        print("No tab found")
        return 0
    
    

if __name__ == '__main__':
    exit(main())


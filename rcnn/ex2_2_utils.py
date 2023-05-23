import os
import platform
import argparse


def get_file_names(folderpath,out='my_notebooks/week2/tmp/output.txt'):
    """ takes a path to a folder and writes all filenames in the folder to a specified output file"""
    res = ""
    out = out or 'my_notebooks/week2/tmp/output.txt'

    for path in os.listdir(folderpath):
        # check if current path is a file
        if os.path.isfile(os.path.join(folderpath, path)):
            res += folderpath+'/'+path+"\n"
    print(res)

    if platform.system() == 'Windows':
        newline=''
    else:
        newline=None
    with open(out, 'w', newline=newline) as output_file:
        output_file.write(res)


def get_all_file_names(filecontent: str, recursive: bool, folderpath, out='my_notebooks/week2/output.txt', saveToFile: bool = False):
    """takes a path to a folder and write all filenames recursively (files of all sub folders to)"""
    
    out = out or 'my_notebooks/week2/output.txt'
    res = []

    for path in os.listdir(folderpath):
        # check if current path is a file
        if os.path.isfile(os.path.join(folderpath, path)):
            filecontent += folderpath.replace('\\', '/')+'/'+path+"\n"
            res.append(folderpath+'\\'+path)
        if os.path.isdir(os.path.join(folderpath, path)):
            filecontent = get_all_file_names(filecontent,True,os.path.join(folderpath, path))

    if recursive == True:
        return filecontent

    if platform.system() == 'Windows':
        newline=''
    else:
        newline=None
    if(saveToFile):
        with open(out, 'w', newline=newline) as output_file:
            output_file.write(filecontent)
            print("Done, go and open: "+out)
    return res


def print_line_one(file_names: list[str]):
    """takes a list of filenames and print the first line of each"""
    with open(file_names) as file_object:
        contents = file_object.read()

    lines = contents.split('\n')

    for line in lines:
        if os.path.isfile(line):
            with open(line) as f_object:
                fcontents = f_object.read()
                flines = fcontents.split('\n')
                print(flines[0])


def print_emails(file_names):
    """takes a list of filenames and print each line that contains an email (just look for @)"""
    with open(file_names) as file_object:
        contents = file_object.read()

    lines = contents.split('\n')

    for line in lines:
        if os.path.isfile(line):
            with open(line) as f_object:
                fcontents = f_object.read()
                flines = fcontents.split('\n')
                for ffline in flines:
                    if ("@" in ffline):
                        print(ffline)


def write_headlines(md_files, out='my_notebooks/week2/tmp/mdoutput.txt'):
    """takes a list of md files and writes all headlines (lines starting with #) to a file"""

    out = out or 'my_notebooks/week2/tmp/mdoutput.txt'
    res = ""

    with open(md_files) as file_object:
        contents = file_object.read()

    lines = contents.split('\n')

    for line in lines:
        if os.path.isfile(line) and ".md" in line:
            with open(line) as f_object:
                fcontents = f_object.read()
                flines = fcontents.split('\n')
                for ffline in flines:
                    if ("#" in ffline):
                        res += ffline+"\n"
    print(res)

    if platform.system() == 'Windows':
        newline=''
    else:
        newline=None
    with open(out, 'w', newline=newline) as output_file:
        output_file.write(res)


if __name__ == '__main__':
    print('2.2.1.1. get_file_names')
    get_file_names('C:/Users/bruger/Desktop/Cph/Semester_4/Python_DataScience/docker_notebooks/notebooks/my_notebooks/week2/tmp')
    print('-------------------\n')

    print('2.2.1.2. get_all_file_names')
    get_all_file_names("", False, 'C:/Users/bruger/Desktop/Cph/Semester_4/Python_DataScience/docker_notebooks/notebooks/my_notebooks/week2')
    print('-------------------\n')

    print('2.2.1.3. print_line_one')
    print_line_one('C:/Users/bruger/Desktop/Cph/Semester_4/Python_DataScience/docker_notebooks/notebooks/my_notebooks/week2/tmp/output.txt')
    print('-------------------\n')
    
    print('2.2.1.4. print_emails')
    print_emails('C:/Users/bruger/Desktop/Cph/Semester_4/Python_DataScience/docker_notebooks/notebooks/my_notebooks/week2/tmp/output.txt')
    print('-------------------\n')

    print('2.2.1.5. write_headlines')
    write_headlines('C:/Users/bruger/Desktop/Cph/Semester_4/Python_DataScience/docker_notebooks/notebooks/my_notebooks/week2/tmp/output.txt')
    print('-------------------\n')



    print('2.2.2')
    parser = argparse.ArgumentParser(description='Exercise 02 - 2.2')
    parser.add_argument('function', help='The function to be used, there are the following: get_file_names, get_all_file_names, print_line_one, print_emails, write_headlines')
    parser.add_argument('path', help='The path to file or folder')
    parser.add_argument('--file', 'outfilename', help='The file for output')
    args = parser.parse_args()

    print('path: ', args.path)

    outputfile = args.outfilename

    if(args.function == 'get_file_names'):
        get_file_names(args.path, outputfile)
    if(args.function == 'get_all_file_names'):
        get_all_file_names(args.path, outputfile)
    if(args.function == 'print_line_one'):
        print_line_one(args.path)
    if(args.function == 'print_emails'):
        print_emails(args.path)
    if(args.function == 'write_headlines'):
        write_headlines(args.path, outputfile)


    
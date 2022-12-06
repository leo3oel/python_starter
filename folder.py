import subprocess as sub

"""
list files
-> Seperate Files and Folders
-> Sort Files and Folders
"""

def getFolders(path):
    command_result = sub.run(["ls", path], capture_output=True, encoding='UTF-8')
    str_result = command_result.stdout

    list = []
    temp = ""

    # Make list with Folder & Filenames
    for i in range(len(str_result)):
        if str_result[i] == "\n":
            list.append(temp)
            temp = ""
        else:
            temp += str_result[i]

    folder = [".."]

    # Separate files with ending from folders
    for item in list:
        for i in range(len(item)):
            if item[i] == ".":
                break
            else:
                if i == len(item)-1:
                    folder.append(item)

    folder.sort()
    return(folder)

# return files list
def getFiles(path, filename):
    command_result = sub.run(["ls", path], capture_output=True, encoding='UTF-8')
    str_result = command_result.stdout

    list = []
    temp = ""

    # Make list with Folder & Filenames
    for i in range(len(str_result)):
        if str_result[i] == "\n":
            list.append(temp)
            temp = ""
        else:
            temp += str_result[i]

    files = []

    # Separate files with ending from folders
    for item in list:
        for i in range(len(item)):
            if item[i] == ".":
                files.append(item)
                break
            else:
                if i == len(item)-1:
                    break

    # count unnecessary items
    delete = []
    for i in range(len(files)):
        item = files[i]
        filenamestart = - len(filename)
        if item[filenamestart:] == filename:
            pass
        else:
            delete.append(i)

    # delete unnecessary items
    offset = 0
    for i in range(len(delete)):
        files.pop(delete[i]-offset)
        offset+=1

    files.sort()

    return(files)
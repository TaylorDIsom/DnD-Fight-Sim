import os

dir = "E:\Library\Computing"
os.chdir(dir)
# cwd = os.getcwd()
# print(cwd)

# dirList = os.listdir(dir)
# scanList = os.scandir(dir)
# print(scanList)

walk = os.walk(dir, True)

def getDirDepth(root, path):
    depth = 0
    rootLen = len(root)
    subDir = path[rootLen:]
    for char in subDir:
        if char == '\\':
            depth += 1
    return depth

tab = "\t"
newLine = "\n"

catFile = open("catalogue.txt", "a")
catFile.write("Library Catalogue\n\n")
for root, dirs, files in walk:
    if len(files) > 0:
        depth = getDirDepth(dir, root)
        dirString = tab*depth + root + newLine
        catFile.write(dirString)
        depth += 1
        for file in files:
            fileString = tab*depth + file + newLine
            catFile.write(fileString)
    catFile.write(newLine)

catFile.close()

import os

with open("file_list.txt", "w") as tempFile:
    for path, subdirs, files in os.walk(r'.\\output\\output'):
       for filename in files:
         s = "<file>offline_tiles/" + filename + "</file>"
         tempFile.write(str(s) + os.linesep) 
print("Done!")
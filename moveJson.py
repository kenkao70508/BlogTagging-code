import os, json, pdb

# Purpose: move large json file to userData_LargeFiles_allDone.
# Reason:  can't upload file's size bigger than 100MB.

userDataPath = '../userData/'
noFolder = ['.git', 'checkJson.py']
userfolders  = [name for name in os.listdir(userDataPath) if name not in noFolder]

def moveJson(filepath, foldername):
    jsonFiles = [filename for filename in os.listdir(filepath) if filename.endswith('.json')]
    for filename in jsonFiles:
        #pdb.set_trace()
        os.system('mkdir userData_LargeFiles_allDone/' + foldername)
        os.system('mv ' + filepath + '/' + filename + ' ../userData_LargeFiles_allDone/' + foldername + '/' )

for folder in userfolders:
    moveJson(userDataPath + folder, folder)

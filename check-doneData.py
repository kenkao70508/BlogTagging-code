import os, json

path_to_doneData = '../doneData/'
jsonFilesIndoneData = [ jsonFile for jsonFile in os.listdir(path_to_doneData) ]
totalNumber = 0

for file in jsonFilesIndoneData:
    with open(path_to_doneData + file, 'r') as f: 
        read_json = json.load(f)
        totalNumber += len(read_json)
        print("FileName:{} ; NumberofArticles:{}".format(path_to_doneData + file, len(read_json)))

print("Total:", totalNumber)


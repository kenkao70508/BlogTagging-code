import os, json

path_to_doneData = '../doneData/'
jsonFilesIndoneData = [ jsonFile for jsonFile in os.listdir(path_to_doneData) ]

print(jsonFilesIndoneData)

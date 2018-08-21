import os, json
import pandas as pd


def updateJsonFile(filename, filepath):

    # update articles keys
    with open(filepath + filename, 'r') as json_file:
        readJson = json.load(json_file)
        print(filepath + filename, readJson[0].keys())
        for item in readJson:
            item['assigned']  = "no"
            item['annotater'] = ""
            item['stored'] = "no"

    with open(filepath + filename, 'w') as json_file2:
        json.dump(readJson, json_file2)

if __name__ == '__main__':
    # path_to_json = '../appierData/appierData/parsedData/'
    # json_files = [pos_json for pos_json in os.listdir(path_to_json) if pos_json.endswith('.json')]
    # for file in json_files:
    #     updateJsonFile(file, path_to_json)    
    path_to_userData = '../userData/'
    userData_folders = [name for name in os.listdir(path_to_userData) if os.path.isdir(os.path.join(path_to_userData,name))]

    for folderName in userData_folders: 
        path_to_userData_user = path_to_userData + folderName + '/'  
        user_categories = [name for name in os.listdir(path_to_userData_user) if os.path.isdir(os.path.join(path_to_userData_user,name))]
        print(user_categories)
    


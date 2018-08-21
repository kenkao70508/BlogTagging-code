import os, json

def Redistribute(filepath):
    json_files = [ pos_json for pos_json in os.listdir(filepath) if pos_json.endswith('.json')]
    print(json_files)
    for file in json_files:
        category = file.split('_')[0]
        os.system('mkdir ' + filepath + category)
        open_file_path = filepath + file
        with open(open_file_path, 'r') as original_file:
            original_data = json.load(original_file)
            for article in original_data:
                saved_path = filepath + category + '/' + category + '_nobackup_' + article['id'] + '.json' 
                JsonDump([article], saved_path)
    return

def JsonDump(data, filepath):
    with open(filepath , 'w') as f: json.dump(data, f)
    return

if __name__ == '__main__':
    path_to_json = '../userData/'
    user_folders = [(pos_json + '/') for pos_json in os.listdir(path_to_json) if pos_json != '.DS_Store']

    original_path = path_to_json + 'user2/'
    Redistribute(original_path)
    # for folder in user_folders:
    #     original_path = path_to_json + folder 
    #     Redistribute(original_path)

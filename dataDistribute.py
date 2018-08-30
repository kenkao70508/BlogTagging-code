import os, pdb, json, argparse

# Given Information:
# - Category: ex. beauty
# - UserNum: ex. user10
# - NumOfArticles: ex. 10

def arg_parse():
    parser = argparse.ArgumentParser()
    parser.add_argument('--user', default='user0', type=str, help='select user')
    parser.add_argument('--cat', default='beauty', type=str, help='select category')
    parser.add_argument('--num', default=0, type=int, help='assign number of articles')
    return parser.parse_args()


def JsonLoad(category, AssignNumber, username):
    print(category, AssignNumber, username)
    path_to_appier_json = '../appierData/appierData/parsedData/'
    path_to_user_json   = '../userData/' + username + '/'
    data_to_be_assigned = []
    
    appier_json_files = [pos_json for pos_json in os.listdir(path_to_appier_json) if pos_json.endswith('.json')]

    # sort json files from small num to large num. 
    # pdb.set_trace()
    appier_json_files_num = [int(filename[len(category):-len('.json')]) for filename in appier_json_files if filename[:len(category)]==category]
    appier_json_files_num.sort()
    
    # set initiate file number as 0:
    IntiateFileNum = -1
    
    # check if the json file contains enough articles to assign.
    temp_assigned_num  = 0
    total_assigned_num = 0
    
    while total_assigned_num < AssignNumber:
        temp_assigned_num = 0
        temp_already_assigned_num = 0
        IntiateFileNum += 1
        # pdb.set_trace()
        target_json_filename = category + str(appier_json_files_num[IntiateFileNum])
        target_json_filepath = path_to_appier_json + category + str(appier_json_files_num[IntiateFileNum]) + '.json'
        no_more_articles_to_be_assigned = True
        
        with open(target_json_filepath, 'r') as read_file:
            temp_data = json.load(read_file)
            num_of_assigned = 0
            
            # assign articles to user's folder
            for article_order in range(len(temp_data)):
                temp_already_assigned_num += 1
                if temp_data[article_order]['assigned'] == 'no':
                    temp_data[article_order]['assigned'] = 'yes'
                    temp_data[article_order]['annotater'] = username
                    saved_path = path_to_user_json + category + '/' + category + str(appier_json_files_num[IntiateFileNum]) + '_' + temp_data[article_order]['id'] + '.json'
                    
                    # save an article to the user folder 
                    JsonDump([temp_data[article_order]], saved_path)
                    total_assigned_num += 1
                    temp_assigned_num += 1
                    if total_assigned_num >= AssignNumber:
                        no_more_articles_to_be_assigned = False
                        break
            print("="*20)
            print("file:", target_json_filepath)
            print("Total Number of articles:", len(temp_data))
            print("Number of assigned articles for this time:", temp_assigned_num)
            print("Number of already assigned articles for current file:", temp_already_assigned_num)
            print("Number of unassigned articles for current file:", len(temp_data) - temp_already_assigned_num)
        
        if no_more_articles_to_be_assigned:
            os.system('rm ' + target_json_filepath)
            target_json_filepath = path_to_appier_json + 'all_assigned/' + category + str(appier_json_files_num[IntiateFileNum]) + '.json'
        
        JsonDump(temp_data, target_json_filepath)

    return 



def JsonDump(data, filepath):
    with open(filepath , 'w') as f: json.dump(data, f)
    return


if __name__ == '__main__':
    args = arg_parse()
    JsonLoad(args.cat, args.num, args.user)
# CheckProcess(LoadData, UpdatedData)





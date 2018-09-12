import csv, os, json, argparse, pdb, datetime
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
from datetime import datetime

# get argument from command
def arg_parse():
    parser = argparse.ArgumentParser()
    parser.add_argument('--user', default='user0', type=str, help='select user')
    parser.add_argument('--n_user', default=0, type=int, help='select user')
    # organize: organize userData to doneData.
    parser.add_argument('--organize', action='store_true',help='')
    parser.add_argument('--statistics', action='store_true',help='')
    parser.add_argument('--userprogress', action='store_true',help='')
    return parser.parse_args()

def openJson(filepath):
    with open(filepath, 'r') as f: data = json.load(f)
    return data

def writeCsv(data, filename):
    with open(filename, 'w', encoding='utf8') as f:
        w = csv.writer(f)
        w.writerows(data)
    return

def tag_count(article, tag):
    soup = BeautifulSoup(article, "html.parser")
    return soup.find_all(tag)

def csv_count(d):
    result = [d['title']]
    for tag in ['content_w','content_s']:
        count = [0,0,0,0,0,0]   
        soup = BeautifulSoup(d[tag], "html.parser")
        for mention in soup.find_all('mention'):
            count[int(mention['score'])]+=1
        for i in range(5,0,-1): result.append(count[i])
    return result

# user annotation analysis
def getStatistics(userPath, user):
    # Show Information
    print("="*30)
    print("user:{}".format(user))
    print("userPath:{}".format(userPath))

    userCsv = []
    CategoryList = ['movie', 'tech', 'beauty', 'food']

    dirInUserPath = os.listdir(userPath)
    if '.DS_Store' in dirInUserPath: dirInUserPath.remove('.DS_Store')
    categoryInfo  = [[(userPath + name + '/'), name] for name in dirInUserPath if\
                    os.path.isdir(os.path.join(userPath,name))]
    
    
    # Initialize Variable
    totalWordTags = 0
    toatlSentenceTags = 0
    totalWords = 0 # total length of tagged articles
    taggedWordList = []
    taggedSentenceList = []
    sumCategoryAnalysis = []

    for cat in categoryInfo:
        print("category:{}".format(cat[1]))
        filePath = [(cat[0] + name) for name in os.listdir(cat[0]) if name.endswith('.json')]
        # Get the information from the article
        for fPath in filePath:
            d = openJson(fPath)[0]

            if d['status']=='tagged':
                print("fileName:{}".format(fPath))
                totalWords  += d['word_count']
                # soup: tagged words & tagged sentence
                taggedWordSoup = tag_count(d['content_w'], 'mention')
                taggedSentenceSoup = tag_count(d['content_s'], 'mention')

                # append tagged text into list
                for taggedWord in taggedWordSoup:
                    taggedWordList.append(taggedWord.text)
                for taggedSentence in taggedSentenceSoup:
                    taggedSentenceList.append(taggedSentence.text)
                

        totalWordTags = len(taggedWordList)
        toatlSentenceTags = len(taggedSentenceList)
        lengthTaggedWordList = [len(word) for word in taggedWordList]
        lengthTaggedSentenceList = [len(sentence) for sentence in taggedSentenceList]
        
        categoryAnalysis = [ user, cat[1],\
            "No Word tags" if totalWordTags==0 else float(totalWords/totalWordTags),\
            "No Sentence tags" if totalWordTags==0 else float(totalWords/toatlSentenceTags),\
            "No Word tags" if len(lengthTaggedWordList)==0 else float(sum(lengthTaggedWordList)) / len(lengthTaggedWordList),\
            "No Sentence tags" if len(lengthTaggedSentenceList)==0 else float(sum(lengthTaggedSentenceList)) / len(lengthTaggedSentenceList)]
    
        # append category analysis to sum
        sumCategoryAnalysis.append(categoryAnalysis)

    return sumCategoryAnalysis

    


if __name__ == '__main__':
    
    args = arg_parse()
    allUserSummary = [['username','category','words/tag_w','words/tag_s','avg_len_tagged_word','avg_len_tagged_sentence']]
    categorySummary = [['username','category','words/tag_w','words/tag_s','avg_len_tagged_word','avg_len_tagged_sentence']]
    
    foodSummary  = [categorySummary[0]]
    movieSummary = [categorySummary[0]] 
    techSummary  = [categorySummary[0]]
    beautySummary  = [categorySummary[0]]

    currentTime = datetime.today()
    timeString  = datetime.now().strftime("%Y%m%d")

    for i in range(args.n_user+1):
        # username
        user = 'user' + str(i)
        # user folder's path
        userPath = '../userDataBackup_180911/' + user + '/'
        # userPath = './userData/' + user + '/'
        userSummary = getStatistics(userPath, user)
        # pdb.set_trace()
        # allUserSummary
        for userCatInfo in userSummary:
            if userCatInfo[1] == 'beauty':
                beautySummary.append(userCatInfo)
            if userCatInfo[1] == 'food':
                foodSummary.append(userCatInfo)
            if userCatInfo[1] == 'movie':
                movieSummary.append(userCatInfo)
            if userCatInfo[1] == 'tech':
                techSummary.append(userCatInfo) 
            allUserSummary.append(userCatInfo)

    # writeCsv(allUserSummary, 'test.csv')
    writeCsv(beautySummary, './generated_csv/beauty_annotate_analysis_' + timeString +'.csv')
    writeCsv(foodSummary, './generated_csv/food_annotate_analysis_' + timeString +'.csv')
    writeCsv(movieSummary, './generated_csv/movie_annotate_analysis_' + timeString +'.csv')
    writeCsv(techSummary, './generated_csv/tech_annotate_analysis_' + timeString +'.csv')
    writeCsv(allUserSummary, './generated_csv/alluser_annotate_analysis_' + timeString +'.csv')



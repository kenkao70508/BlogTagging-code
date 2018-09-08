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

# return category's name
def category(filename):
	if 'movie' in filename: return 'movie'
	elif 'beauty' in filename: return 'beauty'
	elif 'tech' in filename: return 'tech'
	elif 'food' in filename: return 'food'

# return files' directories
def getFileDir(folderpath):
	return FileDir

# return the goal of username
def getGoal(username):
	Goal120User  = ['user0', 'user1', 'user2']
	Goal100User  = ['user11', 'user17']
	if user in Goal120User:
		goal = 120
	elif user in Goal100User:
		goal = 100
	else:
		goal = 50
	return goal

def csv_count(d):
	result = [d['title']]
	for tag in ['content_w','content_s']:
		count = [0,0,0,0,0,0]	
		soup = BeautifulSoup(d[tag], "html.parser")
		for mention in soup.find_all('mention'):
			count[int(mention['score'])]+=1
		for i in range(5,0,-1): result.append(count[i])
	return result

def tag_count(article, tag):
	soup = BeautifulSoup(article, "html.parser")
	return len(soup.find_all(tag))

# create csv files
def writeCsv(data, filename):
	with open(filename, 'w', encoding='utf8') as f:
		w = csv.writer(f)
		w.writerows(data)
	return

def openJson(filepath):
	with open(filepath, 'r') as f: data = json.load(f)
	return data

def writeJson(filepath, data):
	with open(filepath, 'w') as f: json.dump(data, f)
	return 	

# organize data to doneData
def dataOrganize(userPath, donePath):
	# Get Category Info: [[catPath, catName],...]
	categoryInfo = [[(userPath + name + '/'), name] for name in os.listdir(userPath) if\
	                os.path.isdir(os.path.join(userPath,name))]
	
	### Show User Information: ###
	print("*" * 30)
	print("userPath:{}".format(userPath))
	print("donePath:{}".format(donePath))

	for cat in categoryInfo:
		### open doneData##
		# for user11
		if cat[1] == 'beauty_alldone': 
			doneDataPath = donePath + 'beauty.json'
		# for user17
		elif cat[1] == 'movie_alldone':
			doneDataPath = donePath + 'movie.json'
		else:
			doneDataPath = donePath + cat[1] + '.json'
		doneData = openJson(doneDataPath)

		# get filePath
		# num of saved articles
		numOfSavedArticles = 0
		filePath = [(cat[0] + name) for name in os.listdir(cat[0]) if name.endswith('.json')]
		for fPath in filePath:
			article = openJson(fPath)[0]
			article['stored'] = 'no'
			if (article['status'] == 'tagged') & (article['stored'] == 'no'):
				article['stored'] = 'yes'
				doneData.append(article)
				numOfSavedArticles += 1
			# save updated article's information.
			writeJson(fPath, [article])
		# save doneData.
		writeJson(doneDataPath, doneData)

		### Show Saving Information ###
		print("-" * 20)
		print("Category:{}".format(cat[1]))
		print("DoneDataPath:{}".format(doneDataPath))
		print("Num of articles saved to doneData:{}".format(numOfSavedArticles))
		print("-" * 20)

	return 

# record user's tagging process
def recordProgress(userPath, user):
    # record: tags on top of csv.
	workcsv = [['user', 'category', 'goal', 'tagged', 'left']]
	# different categories of articles
	CategoryList = ['movie', 'tech', 'beauty', 'food']
	totalDone = 0
	
	# Get the goal of the user
	goal = getGoal(user)
	# Count number of tagging articles
	progress = 0
	# Count number of tagged articles
	done = 0
		
	# Get Category Info: [[catPath, catName],...]
	categoryInfo = [[(userPath + name + '/'), name] for name in os.listdir(userPath) if\
	                os.path.isdir(os.path.join(userPath,name))]
	
	for cat in categoryInfo:
		# Get file path
		filePath = [(cat[0] + name) for name in os.listdir(cat[0]) if name.endswith('.json')]
		
		for fPath in filePath:
			article = openJson(fPath)[0]
			if (article['status'] == 'tagged'):
				done += 1
			elif (article['status'] == 'tagging'):
				progress += 1
	
	# Count the number of tagged articles.
	totalDone += done

	# Show the progress of the specific user
	print("User: {}; result:{}".format(user, [user, goal, progress, done, goal-done]))
	return [user, goal, progress, done, goal-done]

# Get doneData's statistics

def getStatistics():
	done_path = '../doneDataBackup_180904/'
	files = os.listdir(os.path.join(os.getcwd(), done_path))
	abd_csv = [['category','average_chars_per_abandoned_article','average_chars_per_tagged_article','abandoned_ratio']]
	total_csv = [['category','done_articles','tagged_sentences','sentence_five','sentence_four','sentence_three','sentence_two','sentence_one','tagged_words','word_five','word_four','word_three','word_two','word_one']]
	print("Files in the folder:{}".format(files))
	for filename in files:
		csvc = [['title','sentence_five','sentence_four','sentence_three','sentence_two','sentence_one','word_five','word_four','word_three','word_two','word_one']]
		data = openJson(done_path+filename)

		# Show Information
		print("Number of articles:{}".format(len(data)))
		# pdb.set_trace()
		tagged_w = 0
		tagged_s = 0
		tagged_n = 0
		w = [0]*6
		s = [0]*6
		tagged_words = 0
		
		abandoned_words = 0
		abandoned_n = 0
		
		for d in data:
			print(d['id'], d['status'])
			if d['status']=='tagged':
				tagged_words += tag_count(d['content_w'],'word')
				tagged_w+=tag_count(d['content_w'],'mention')
				tagged_s+=tag_count(d['content_s'],'mention')
				tagged_n+=1
				c = csv_count(d)
				for i in range(1,6): s[i]+=c[i]
				for i in range(6,11): w[i-5]+=c[i]
				csvc.append(c)
			elif d['status']=='abandoned':
				abandoned_words+=tag_count(d['content_w'],'word')
				abandoned_n+=1
		sum_s = s[1]+s[2]+s[3]+s[4]+s[5]
		sum_w = w[1]+w[2]+w[3]+w[4]+w[5]
		#abd_csv.append([category(filename), abandoned_words/abandoned_n, tagged_words/tagged_n, abandoned_n/len(data)])
		total_csv.append([category(filename), tagged_n, sum_s, s[5]/sum_s, s[4]/sum_s, s[3]/sum_s, s[2]/sum_s, s[1]/sum_s, sum_w, w[5]/sum_w, w[4]/sum_w, w[3]/sum_w, w[2]/sum_w, w[1]/sum_w])
		writeCsv(csvc, csv_path+category(filename)+'_done_gereralInfo_'+ timeString + '.csv')
	writeCsv(abd_csv, csv_path+'abandoned_analysis_' + timeString + '.csv')
	writeCsv(total_csv, csv_path+'total_analysis_' + timeString + '.csv')	



if __name__ == '__main__':
	args = arg_parse()
	totalDone = 0
	csv_path = './generated_csv/'
	workcsv = [['user', 'category', 'goal', 'tagged', 'left']]
	timeString  = datetime.now().strftime("%Y%m%d")
	
	# Number of users.
	for i in range(args.n_user+1):
		# username
		user = 'user' + str(i)
		# user folder's path
		userPath = '../userDataBackup_180904/' + user + '/'
		# done folder's path
		donePath = '../doneDataBackup_180904/'

		if args.organize:
			dataOrganize(userPath, donePath)
		
		elif args.userprogress:
		    # tags on top of csv.
			userStatus = recordProgress(userPath, user)
			workcsv.append(userStatus)

	# Get statistics.
	if args.statistics:
		getStatistics()

	# Save all users progress
	if args.userprogress:
		writeCsv(workcsv, csv_path + 'alluser_status_' + timeString + '.csv')






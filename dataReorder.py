import csv, os, json, argparse
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
import pdb

def arg_parse():
	parser = argparse.ArgumentParser()
	parser.add_argument('--user', default='user0', type=str, help='select user')
	parser.add_argument('--n_user', default=1, type=int, help='select user')
	# organize: organize userData to doneData.
	parser.add_argument('--organize', action='store_true',help='')
	parser.add_argument('--count', action='store_true',help='')
	parser.add_argument('--alluser', action='store_true',help='')
	return parser.parse_args()
def category(filename):
	if 'movie' in filename: return 'movie'
	elif 'beauty' in filename: return 'beauty'
	elif 'tech' in filename: return 'tech'
	elif 'food' in filename: return 'food'

def csv_count(d):
	result = [d['title']]
	for tag in ['content_w','content_s']:
		count = [0,0,0,0,0,0]
		#root = ET.fromstring(d[tag])	
		soup = BeautifulSoup(d[tag], "html.parser")
		for mention in soup.find_all('mention'):
			#print(mention['score'])
			count[int(mention['score'])]+=1
		for i in range(5,0,-1): result.append(count[i])
	return result
def tag_count(article, tag):
	soup = BeautifulSoup(article, "html.parser")
	return len(soup.find_all(tag))
def csv_write(data, filename):
	with open(filename, 'w', encoding='utf8') as f:
		w = csv.writer(f)
		w.writerows(data)
	return
		
args = arg_parse()
csv_path = 'generated_csv/'
if args.alluser:
	workcsv = [['user','goal','tagging','tagged','left']]
	for i in range(args.n_user+1):
		user = 'user'+str(i)
		user_path = '../userData/'+user
		goal = 50
		progress = 0
		done = 0
		#abandoned = 0
		print(user)
		files = os.listdir(os.path.join(os.getcwd(), user_path))
		for filename in files:
			if not filename.endswith('.json'): continue
			with open(user_path+'/'+filename, 'r',encoding='utf8') as f: data = json.load(f)
			for d in data:
				if d['status']=='tagged': done+=1
				elif d['status']=='tagging': progress+=1 
				#elif d['status']=='abandoned': abandoned+=1
		workcsv.append([user,goal,progress,done,goal-done])
		with open(csv_path+'alluser_status.csv', 'w', encoding='utf8') as f:
			w = csv.writer(f)
			w.writerows(workcsv)
elif args.count:
	done_path = '../doneData/first_stage/'
	files = os.listdir(os.path.join(os.getcwd(), done_path))
	abd_csv = [['category','average_chars_per_abandoned_article','average_chars_per_tagged_article','abandoned_ratio']]
	total_csv = [['category','done_articles','tagged_sentences','sentence_five','sentence_four','sentence_three','sentence_two','sentence_one','tagged_words','word_five','word_four','word_three','word_two','word_one']]
	for filename in files:
		print(filename)
		csvc = [['title','sentence_five','sentence_four','sentence_three','sentence_two','sentence_one','word_five','word_four','word_three','word_two','word_one']]
		with open(done_path+filename, 'r') as f: data = json.load(f)
		tagged_w = 0
		tagged_s = 0
		tagged_n = 0
		w = [0]*6
		s = [0]*6
		tagged_words = 0
		#abandoned_words = 0
		#abandoned_n = 0
		
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
			#elif d['status']=='abandoned':
				#abandoned_words+=tag_count(d['content_w'],'word')
				#abandoned_n+=1
		sum_s = s[1]+s[2]+s[3]+s[4]+s[5]
		sum_w = w[1]+w[2]+w[3]+w[4]+w[5]
		#abd_csv.append([category(filename), abandoned_words/abandoned_n, tagged_words/tagged_n, abandoned_n/len(data)])
		total_csv.append([category(filename), tagged_n, sum_s, s[5]/sum_s, s[4]/sum_s, s[3]/sum_s, s[2]/sum_s, s[1]/sum_s, sum_w, w[5]/sum_w, w[4]/sum_w, w[3]/sum_w, w[2]/sum_w, w[1]/sum_w])
		csv_write(csvc, csv_path+category(filename)+'_done_gereralInfo.csv')
	csv_write(abd_csv, csv_path+'abandoned_analysis.csv')
	csv_write(total_csv, csv_path+'total_analysis.csv')
# organize: 
elif args.organize:
	# done_path: path to store tagged articles.
	done_path = '../doneData/first_stage/'

	for cate in ['food','tech','beauty','movie']:
		with open(done_path+cate+'.json', 'w') as f: json.dump([],f)
	# pdb.set_trace()
	for i in range(args.n_user+1):
		user_path = '../userData/user'+str(i)+'/'
		user_files = os.listdir(os.path.join(os.getcwd(), user_path))
		
		for userf in user_files:
			if not userf.endswith('.json'): continue
			print('user{}/{}'.format(i,userf))
			with open(user_path+userf,'r',encoding='utf8') as f: userData = json.load(f)
			with open(done_path+category(userf)+'.json','r') as f: doneData = json.load(f)
			for d in userData:
				if d['status']!='tagged': continue 
				d['annotator'] = args.user
				doneData.append(d)
			with open(done_path+category(userf)+'.json', 'w') as f: json.dump(doneData,f)

import csv, os, json, argparse, pdb, datetime
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
from datetime import datetime 

def tag_count(article, tag):
    soup = BeautifulSoup(article, "html.parser")
    return soup.find_all(tag)

newData = []

with open('food.json', 'r') as f:
##### get content strings #####
    data = json.load(f)
    articleStringList = []
    string = ''
    print(len(data))
    for article in data:
        sentences = tag_count(article['content_s'], 'word')
        for s in sentences:
            if " " in s.text:
                if string != "":
                    articleStringList.append(string)
                    string = ''
                    continue
                else:    
                    continue
            string += s.text
        # print(articleStringList)

    ##### get [score, sentence] #####
        scoreSentenceList = []
        sentences = tag_count(article['content_s'], 'mention')
        for s in sentences:
            cleanS = s.text.replace(" ", "")
            scoreSentenceList.append([int(s['score']),cleanS])
        # print(scoreSentenceList)
    ##### get [score, word] #####
        scoreWordList = []
        words = tag_count(article['content_w'], 'mention')
        for w in words:
            cleanW = w.text.replace(" ", "")
            scoreWordList.append([int(w['score']),cleanW])
        # print(scoreWordList)
        article.update({'articleStringList':articleStringList,'scoreSentenceList':scoreSentenceList, 'scoreWordList':scoreWordList})

with open('food_refine.json', 'w') as f2: 
    json.dump(data, f2)








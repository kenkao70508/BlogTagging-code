import sqlite3
import csv
import argparse

def arg_parse():
    parser = argparse.ArgumentParser()
    parser.add_argument('--user', default='user0', type=str, help='select user')
    parser.add_argument('--cat', default='beauty', type=str, help='select user')
    return parser.parse_args()

def create():
    with open('./data/user.csv', newline='') as f:
        csv_reader = csv.DictReader(f)
        user = [(row['username'], row['password'], '') for row in csv_reader]

    with open('schema.sql') as f:
        sql = f.read()

    db = sqlite3.connect('user.db')
    with db:
        db.executescript(sql)
        db.executemany(
            'INSERT INTO  user (username, password, category) VALUES (?, ?, ?)', user
        )

def view():
    db = sqlite3.connect('user.db')
    with db:
        data = db.execute('SELECT * FROM user')
    for row in data:
        print(row)

def updateCat(user, category):
    db = sqlite3.connect('user.db')
    with db:
        db.execute(
            'UPDATE user SET category = ?  WHERE username= ? ',
            (category, user)
        )

def example():
## this is an example showing how to update category list for user 'guest'
    updateCat('user0', 'tech_0')

if  __name__ == '__main__':
    arg = arg_parse()
    updateCat(arg.user, arg.cat)
    view()
    

#!/usr/bin/env python3
# -*- coding:utf-8 -*-
from flask import (
    Flask, jsonify, render_template, request, send_from_directory, url_for, 
    g, redirect, session, 
)
import json, os, sqlite3,pdb

app = Flask(__name__)
SQLITE_DB_PATH = 'user.db'
SQLITE_DB_SCHEMA = 'schema.sql'
MEMBER_CSV_PATH = './data/user.csv'
app.secret_key = 'd7e977e3b75db569238259291645ceefde9dd89c3c6a5365'

@app.route('/', methods=['GET', 'POST'])
def main():
    return render_template('home.html')

@app.route('/category/<category>', methods=['GET', 'POST'])
def category(category):
    ##  找到json file的位置
    filepath = getJsonLoc(category)
    json_files = [pos_json for pos_json in os.listdir(filepath) if pos_json.endswith('.json')]    

    ##  collect info for all articles in the category
    articleList = []
    articles = []
    articleType = category
    print("="*10)
    print("action: Load all Json Files")
    for file in json_files:
        with open(filepath + '/' + file, 'r', encoding="utf-8") as f: 
            article = json.load(f)
            articles.append(article[0])
            session[article[0]['id']] = file
            print("message: Session[{}]:{}".format(article[0]['id'], file))
            for a in article: articleList.append([a['id'], a['title'], a['number']])
        f.close()
    
    ## collect data for specific article
    index = request.args.get('index')
    if not index: 
        index = articleList[0][0]
    print("message: This is the current article's index/id:", index)   
    
    for a in articles:
        if a['id'] == index:
            articleName = a['title']
            articleLink = a['link']
            content_s = a['content_s']
            content_w = a['content_w']
            item_name = a['item_name']
            item_store = a['item_store']
            view_count = a['view_count']
            word_count = a['word_count']
            if 'status' not in a:
                a['status'] = 'untagged'
            status = a['status']
            if 'new_title' not in a:
                a['new_title'] = 'none'
            new_title = a['new_title']
            break

    ##  specify allowed article status        
    statusList = ['untagged','tagging','tagged','abandoned']
    print("action: Show article")
    print("="*10)
    return render_template('index.html', article_s=content_s, article_w=content_w, 
    articleIndex=index, articleName=articleName, articleLink=articleLink,
    articleList=articleList, articleType=articleType, view_count=view_count, word_count = word_count,
    item_name=item_name, item_store=item_store, articleStatus=status, statusList=statusList,
    new_title=new_title)


@app.route('/articlelist/<category>', methods=['GET', 'POST'])
def articleList(category):
    ##  locate json file
    filepath = getJsonLoc(category)
    json_files = [pos_json for pos_json in os.listdir(filepath) if pos_json.endswith('.json')]     
    
    ## collect info for all articles in the category
    articleList = []
    articleType = category
    for file in json_files:
        with open(filepath + '/' + file, 'r', encoding="utf-8") as f: 
            articles = json.load(f)
            for a in articles: 
                if 'status' not in a:
                    a['status'] = 'untagged'
                articleList.append([a['id'], a['title'], a['number'], a['status']])
        f.close()
    
    return render_template('articleList.html', articleList=articleList, articleType=articleType)

@app.route('/save', methods=['POST'])
def save():
    try:
        ## get data from user
        content = request.get_json()
        articleType = content['articleType']
        filename = session.get(content['index'])
        ## locate json file
        json_file = getJsonLoc(articleType)
        print("="*10)
        print("action: Save-success ")
        pdb.set_trace()
        print("message: file_path:{}".format(json_file + '/' + filename))

        with open(json_file + '/' + filename, 'r', encoding="utf-8") as f: data = json.load(f)
        for d in data:
            if d['id']==content['index']: 
                d['content_w'] = content['data_w']
                d['content_s'] = content['data_s']
                d['item_name'] = content['item_name']
                d['item_store'] = content['item_store']
                d['status'] = content['status']
                d['new_title'] = content['new_title']
        with open(json_file + '/' + filename, 'w') as f: json.dump(data, f)
        f.close()
        print("action: Saved!")
        print("="*10)
        return jsonify(message='')
    except Exception as e:
        print("="*10)
        print("action: Save-wrong ")
        print("="*10)
        return jsonify(message=str(e)), 500

@app.route('/login', methods=(['GET', 'POST']))
def login():
    try:
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None
        user = db.execute(
            'SELECT * FROM user WHERE username = ?', (username,)
        ).fetchone()

        if user is None:
            error = '帳號或密碼錯誤'
        elif not user[2] == password:
            error = '帳號或密碼錯誤'

        if error is None:
            session.clear()
            session['user_id'] = user[0]
            return redirect(url_for('main'))

        return render_template('login.html', loginError=error)
    except Exception as e:
        return redirect(url_for('main'))


@app.before_request
def load_logged_in_user():
    ## obtain user info before every request
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM user WHERE id = ?', (user_id,)
        ).fetchone()
        g.categoryList = g.user[3].replace(" ", "").split(",")
        g.username = g.user[1]

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('main'))

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(SQLITE_DB_PATH)
    return db


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def getJsonLoc(category):
    try:
        if g.username and category:
            return os.path.join('../userData', str(g.username), str(category))    
        else:
            return os.path.join('data', str(category)+'.json')
    except:
        return os.path.join('data', str(category)+'.json')


if __name__ == '__main__':
    app.run(debug=True, host='140.112.90.203', port=5789)
    # app.run(debug=True)

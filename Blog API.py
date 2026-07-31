from flask import Flask, request, jsonify
import sqlite3
import json
import sys
import os
from datetime import datetime

app = Flask(__name__)

@app.route('/posts', methods=['POST'])
def create_post():

    con =  sqlite3.connect('blog.db')
    cursor = con.cursor()
    data = request.get_json()
    date = datetime.today()
    date_str = date.strftime('%d-%b-%Y, %H:%M')
    tags = data['tags']
    tags_str = json.dumps(tags)

    try:
        cursor.execute('INSERT into posts(title, content, category, tags, created_at, updated_at) VALUES(:title, :content, :category, :tags, :created_at, :updated_at)',
            {'title': data['title'], 'content': data['content'], 'category': data['category'], 'tags': tags_str, 'created_at': date_str, 'updated_at': date_str})
        con.commit()

    except sqlite3.Error as e:

        return jsonify({'error': str(e)}), 400

    new_id = cursor.lastrowid
    return jsonify({'id': new_id, 'title': data['title'], 'content': data['content'], 'category': data['category'], 'tags': data['tags'], 'created_at': date_str, 'updated_at': date_str}), 201

@app.route('/posts/<int:rowid>', methods=['PUT'])
def update_post(rowid):

    con = sqlite3.connect('blog.db')
    cursor = con.cursor()
    data = request.get_json()
    date = datetime.today()
    date_str = date.strftime('%d-%b-%Y, %H:%M')
    tags = data['tags']
    tags_str = json.dumps(tags)

    cursor.execute('SELECT * FROM posts WHERE rowid = :id', {'id':rowid})
    if cursor.fetchone() == None:

        con.close()
        return jsonify({'error': 'Post not found!'}), 404
    
    try:
        cursor.execute('UPDATE posts SET title=:title, content=:content, category=:category, tags=:tags, updated_at=:updated_at  WHERE rowid = :rowid', 
            {'title': data['title'], 'content': data['content'], 'category': data['category'], 'tags': tags_str, 'updated_at':date_str, 'rowid':rowid})
        con.commit()

    except sqlite3.Error as e:

        con.close()
        return jsonify({'error': str(e)}), 400
    
    cursor.execute('SELECT * FROM posts WHERE rowid = :id', {'id':rowid})
    updated_row = cursor.fetchone()
    con.close()
    return jsonify({'id': updated_row[0], 'title': updated_row[1], 'content': updated_row[2], 'category': updated_row[3], 'tags': json.loads(updated_row[4]), 'created_at':updated_row[5], 'updated_at': updated_row[6]}), 200


if __name__=='__main__':
    app.run(debug=True)


    








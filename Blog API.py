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
        cursor.execute('INSERT into posts(title, content, category, tags, created_at, updated_at) VALUES(?, ?, ?, ?, ?, ?)', (data['title'], data['content'], data['category'], tags_str, date_str, date_str))
        con.commit()

    except sqlite3.Error as e:

        return jsonify({'error': str(e)}), 400

    new_id = cursor.lastrowid

    return jsonify({'id': new_id, 'title': data['title'], 'content': data['content'], 'category': data['category'], 'tags': data['tags'], 'created_at': date_str, 'updated_at': date_str}), 201

if __name__=='__main__':
    app.run(debug=True)


    








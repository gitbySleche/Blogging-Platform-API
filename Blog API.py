from flask import Flask, request, jsonify
import sqlite3
import json
from datetime import datetime

app = Flask(__name__)

def post_not_found(post_id):

    con =  sqlite3.connect('blog.db')
    cursor = con.cursor()

    cursor.execute('SELECT * FROM posts WHERE rowid = :id', {'id':post_id})
    if cursor.fetchone() == None:

        con.close()
        return True
    else:
        con.close()
        return False

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

    if post_not_found(rowid):
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

@app.route('/posts/<int:rowid>', methods=['DELETE'])
def delete_post(rowid):

    con = sqlite3.connect('blog.db')
    cursor = con.cursor()

    if post_not_found(rowid):
        return jsonify({'error': 'Post not found!'}), 404

    try:
        cursor.execute('DELETE FROM posts WHERE rowid = :id', {'id':rowid})
        con.commit()

    except sqlite3.Error as e:
        con.close()
        return jsonify({'error': str(e)}), 400

    return '', 204

@app.route('/posts/<int:rowid>', methods=['GET'])
def get_post(rowid):

    con = sqlite3.connect('blog.db')
    cursor = con.cursor()

    if post_not_found(rowid):
        return jsonify({'error': 'Post not found!'}), 404

    cursor.execute('SELECT * FROM posts WHERE rowid = :id', {'id':rowid})
    data = cursor.fetchone()
    con.close()

    return jsonify({'id': data[0], 'title': data[1], 'content': data[2], 'category': data[3], 'tags': json.loads(data[4]), 'created_at':data[5], 'updated_at': data[6]}), 200

@app.route('/posts', methods=['GET'])
def get_all_posts():

    con = sqlite3.connect('blog.db')
    cursor = con.cursor()
    term = request.args.get('term')
    search_term = f"%{term}%"

    if term:
        cursor.execute('SELECT * FROM posts WHERE title LIKE :term OR content LIKE :term OR category LIKE :term', {'term':search_term})
        data = cursor.fetchall()
        con.close()
        new_list = []
        
        for row in data:
        
            if row:
                new_list.append({'id': row[0], 'title': row[1], 'content': row[2], 'category': row[3], 'tags': json.loads(row[4]), 'created_at':row[5], 'updated_at': row[6]})
            
        return jsonify(new_list), 200

    else:
    
        cursor.execute('SELECT * FROM posts')
        data = cursor.fetchall()
        con.close()
        new_list = []

        for row in data:

            if row:
                new_list.append({'id': row[0], 'title': row[1], 'content': row[2], 'category': row[3], 'tags': json.loads(row[4]), 'created_at':row[5], 'updated_at': row[6]})
        
        return jsonify(new_list), 200


if __name__=='__main__':
    app.run(debug=True)


    








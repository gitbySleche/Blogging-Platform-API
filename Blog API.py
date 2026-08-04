from flask import Flask, request, jsonify
import sqlite3
import json
from datetime import datetime

app = Flask(__name__)

def post_not_found(post_id, cursor):
    cursor.execute('SELECT * FROM posts WHERE rowid = :id', {'id':post_id})
    return cursor.fetchone() is None 

@app.route('/posts', methods=['POST'])
def create_post():

    con =  sqlite3.connect('blog.db')
    cursor = con.cursor()
    data = request.get_json()
    date = datetime.today()
    date_str = date.strftime('%d-%b-%Y, %H:%M')
    tags = data.get('tags')
    
    try:
        if 'title' not in data or 'content' not in data or 'category' not in data or tags is None:
            return jsonify({'error': 'Missing fields.'}), 400

        tags_str = json.dumps(tags)  
        cursor.execute('INSERT into posts(title, content, category, tags, created_at, updated_at) VALUES(:title, :content, :category, :tags, :created_at, :updated_at)',
            {'title': data['title'], 'content': data['content'], 'category': data['category'], 'tags': tags_str, 'created_at': date_str, 'updated_at': date_str})
        con.commit()
    

    except sqlite3.Error as e:
        return jsonify({'error': str(e)}), 400

    else:
        new_id = cursor.lastrowid
        return jsonify({'id': new_id, 'title': data['title'], 'content': data['content'], 'category': data['category'], 'tags': data['tags'], 'created_at': date_str, 'updated_at': date_str}), 201

    finally:
        con.close()

@app.route('/posts/<int:rowid>', methods=['PUT'])
def update_post(rowid):

    con = sqlite3.connect('blog.db')
    cursor = con.cursor()
    data = request.get_json()
    date = datetime.today()
    date_str = date.strftime('%d-%b-%Y, %H:%M')
    tags = data['tags']
    tags_str = json.dumps(tags)
    
    try:
        if post_not_found(rowid, cursor):
            return jsonify({'error': 'Post not found!'}), 404
        
        cursor.execute('UPDATE posts SET title=:title, content=:content, category=:category, tags=:tags, updated_at=:updated_at  WHERE rowid = :rowid', 
            {'title': data['title'], 'content': data['content'], 'category': data['category'], 'tags': tags_str, 'updated_at':date_str, 'rowid':rowid})
        con.commit()

    except sqlite3.Error as e:
        return jsonify({'error': str(e)}), 400
    
    else:
        cursor.execute('SELECT * FROM posts WHERE rowid = :id', {'id':rowid})
        updated_row = cursor.fetchone()
        return jsonify({'id': updated_row[0], 'title': updated_row[1], 'content': updated_row[2], 'category': updated_row[3], 'tags': json.loads(updated_row[4]), 'created_at':updated_row[5], 'updated_at': updated_row[6]}), 200

    finally:
        con.close()

@app.route('/posts/<int:rowid>', methods=['DELETE'])
def delete_post(rowid):

    con = sqlite3.connect('blog.db')
    cursor = con.cursor()

    try:
        if post_not_found(rowid, cursor):
            return jsonify({'error': 'Post not found!'}), 404
        
        cursor.execute('DELETE FROM posts WHERE rowid = :id', {'id':rowid})
        con.commit()

    except sqlite3.Error as e:
        return jsonify({'error': str(e)}), 400

    else:
        return '', 204

    finally: 
        con.close()

@app.route('/posts/<int:rowid>', methods=['GET'])
def get_post(rowid):

    con = sqlite3.connect('blog.db')
    cursor = con.cursor()

    try:
        if post_not_found(rowid, cursor):
            return jsonify({'error': 'Post not found!'}), 404
        
        cursor.execute('SELECT * FROM posts WHERE rowid = :id', {'id':rowid})
        data = cursor.fetchone()
        return jsonify({'id': data[0], 'title': data[1], 'content': data[2], 'category': data[3], 'tags': json.loads(data[4]), 'created_at':data[5], 'updated_at': data[6]}), 200


    except sqlite3.Error as e:
        return jsonify({'error': str(e)}), 400

    finally: 
        con.close()

@app.route('/posts', methods=['GET'])
def get_all_posts():

    con = sqlite3.connect('blog.db')
    cursor = con.cursor()
    term = request.args.get('term')
    search_term = f"%{term}%"

    try:
        new_list = []

        if term:
            cursor.execute('SELECT * FROM posts WHERE title LIKE :term OR content LIKE :term OR category LIKE :term', {'term':search_term})
            data = cursor.fetchall()

        else:
            cursor.execute('SELECT * FROM posts')
            data = cursor.fetchall()
            

        for row in data:

            if row:
                new_list.append({'id': row[0], 'title': row[1], 'content': row[2], 'category': row[3], 'tags': json.loads(row[4]), 'created_at':row[5], 'updated_at': row[6]})
        
        return jsonify(new_list), 200
        
    except sqlite3.Error as e:
        return jsonify({'error': str(e)}), 400
    
    finally: 
        con.close()


if __name__=='__main__':
    app.run(debug=True)


    








#!/usr/bin/env python
# encoding: utf-8
'''
パスワード管理APIサーバー

Copyright (C) 2019 yoya(@amenoyoya). All rights reserved.
GitHub: https://github.com/amenoyoya/password-manager
License: MIT License
'''
from libs.frasco import g, request, Frasco, Response
from libs.sqldb import SqlDB
import os, json, hashlib

class AuthUser:
    ''' 認証処理クラス '''
    @staticmethod
    def auth(post):
        ''' ユーザー認証 '''
        username = post.get('username', '')
        password = post.get('password', '')
        users = get_db().get_rows('users', {
            'select': ['id', 'token', 'username'],
            'where': {
                'and': [
                    {'=': {'username': username}},
                    {'=': {'password': hashlib.sha256(password.encode()).hexdigest()}}
                ]
            }
        })
        if users and len(users) == 1:
            return users[0]
    
    @staticmethod
    def save(user):
        return json.dumps(user)
    
    @staticmethod
    def load(session_id):
        return json.loads(session_id)

# encrypt text by using xor
def encrypt(src_text, key='key'):
    xor_code = key
    while len(src_text) > len(xor_code):
        xor_code += key
    return ''.join(
        [chr(ord(data) ^ ord(code)) for (data, code) in zip(src_text, xor_code)]
    ).encode().hex()

# decrypt text by using xor
def decrypt(hex_text, key='key'):
    try:
        crypt_data = bytes.fromhex(hex_text).decode()
    except ValueError:
        return False
    xor_code = key
    while len(crypt_data) > len(xor_code):
        xor_code += key
    return ''.join(
        [chr(ord(data) ^ ord(code)) for (data, code) in zip(crypt_data, xor_code)]
    )

# 使用するデータベース
DATABASE = os.path.join(os.path.dirname(__file__), 'database', 'password.db')

# Flaskアプリケーション
app = Frasco(__name__, User=AuthUser)

# Databaseのconnectionを取得
def get_db():
    if not hasattr(g, 'databse'):
        g.database = SqlDB(DATABASE)
    return g.database

# 認証処理
@app.auth('/login', '/logout', Response.text('Logged out\n'))
def login(user):
    if user is None:
        return Response.text('Authentication error\n', 400)
    return Response.text('Logged in\n')

# ログインユーザーのパスワード情報を取得
@app.get('/')
@app.secret(Response.text('Unauthenticated\n', 401))
def get_info():
    db = get_db()
    res = {}
    categories = db.get_rows('user_categories', {
        'select': ['id', 'category'],
        'where': {'user_id': app.current_user['id']}
    })
    for category in categories:
        res[category['category']] = db.get_rows('category_passwords', {
            'select': ['service', 'username', 'password', 'remarks'],
            'where': {'=': {'category_id': category['id']}}
        })
        # service と username だけ暗号化解除する
        for row in res[category['category']]:
            row['service'] = decrypt(row['service'])
            row['username'] = decrypt(row['username'])
    return Response.json(res)

# password と remarks の暗号化解除
@app.get('/password')
@app.secret(Response.text('Unauthenticated\n', 401))
def get_password():
    password = request.form.get('password', '')
    remarks = request.form.get('remarks', '')
    return Response.json({
        'password': decrypt(password),
        'remarks': decrypt(remarks)
    })

# 指定カテゴリーIDがログインユーザーの所有か確認
def is_correct_category(db, id):
    categories = db.get_rows('user_categories', {
        'where': {
            'and': [
                {'=': {'id': id}},
                {'=': {'user_id': app.current_user['id']}}
            ]
        }
    })
    if not categories or len(categories) == 0:
        return False
    return True

# 指定IDのパスワード情報を取得
def get_data(db, id):
    data = db.get_rows('category_passwords', {'where': {'=': {'id': id}}})
    if not data or len(data) == 0:
        return False
    return data[0]

# 新規パスワード情報追加
@app.post('/')
@app.secret(Response.text('Unauthenticated\n', 401))
def insert_data():
    category_id = request.form.get('category_id')
    service = request.form.get('service')
    username = request.form.get('username', '')
    password = request.form.get('password', '')
    remarks = request.form.get('remarks', '')
    if category_id is None or service is None:
        # カテゴリーID, サービス名は必須
        return Response.text('Require `category_id` and `service`\n', 400)
    db = get_db()
    # カテゴリーの所有ユーザーか確認
    if not is_correct_category(db, category_id):
        return Response.text('Invalid `category_id`\n', 400)
    # データ追加
    count = db.insert_rows('category_passwords', [
        ['category_id', 'service', 'username', 'password', 'remarks'],
        [category_id, encrypt(service), encrypt(username), encrypt(password), encrypt(remarks)]
    ])
    if count == 0:
        return Response.text('Failed to insert data\n', 500)
    return Response.text('Succeeded to insert data\n', 201)

# パスワード情報修正
@app.put('/<int:data_id>')
@app.secret(Response.text('Unauthenticated\n', 401))
def update_data(data_id):
    service = request.form.get('service')
    username = request.form.get('username', '')
    password = request.form.get('password', '')
    remarks = request.form.get('remarks', '')
    if service is None:
        # サービス名は必須
        return Response.text('Require `service`\n', 400)
    db = get_db()
    # 存在しているデータか確認
    data = get_data(db, data_id)
    if not data:
        return Response.text('Nonexistent data\n', 400)
    # カテゴリーの所有ユーザーか確認
    if not is_correct_category(db, data['category_id']):
        return Response.text('Invalid `data_id`\n', 400)
    # データ更新
    count = db.update_rows('category_passwords', {
        'values': {
            'service': encrypt(service),
            'username': encrypt(username),
            'password': encrypt(password),
            'remarks': encrypt(remarks)
        },
        'where': {'=': {'id': data_id}}
    })
    if count == 0:
        return Response.text('Failed to update data\n', 500)
    return Response.text('Succeeded to update data\n')

# パスワード情報削除
@app.delete('/<int:data_id>')
@app.secret(Response.text('Unauthenticated\n', 401))
def delete_data(data_id):
    db = get_db()
    # 存在しているデータか確認
    data = get_data(db, data_id)
    if not data:
        return Response.text('Nonexistent data\n', 400)
    # カテゴリーの所有ユーザーか確認
    if not is_correct_category(db, data['category_id']):
        return Response.text('Invalid `data_id`\n', 400)
    # データ削除
    count = db.delete_rows('category_passwords', {'where': {'=': {'id': data_id}}})
    if count == 0:
        return Response.text('Failed to delete data\n', 500)
    return Response.text('Succeeded to delete data\n')

# Flaskサーバー実行
if __name__ == "__main__":
    # ログインAPIサーバーは localhost:4000 で実行
    app.run(debug=True, port=4000)

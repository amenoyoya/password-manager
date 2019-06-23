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

def get_db():
    ''' Databaseのconnectionを取得 '''
    if not hasattr(g, 'databse'):
        g.database = SqlDB(DATABASE)
    return g.database

@app.auth('/login', '/logout', Response.text('Logged out\n'))
def login(user):
    ''' 認証処理 '''
    if user is None:
        return Response.text('Authentication error\n', 400)
    return Response.text('Logged in\n')

@app.get('/')
@app.secret(Response.text('Unauthenticated\n', 401))
def get_info():
    ''' ログインユーザーのパスワード情報を取得 '''
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

@app.get('/password')
@app.secret(Response.text('Unauthenticated\n', 401))
def get_password():
    ''' password と remarks の暗号化解除 '''
    password = request.form.get('password', '')
    remarks = request.form.get('remarks', '')
    return Response.json({
        'password': decrypt(password),
        'remarks': decrypt(remarks)
    })

# Flaskサーバー実行
if __name__ == "__main__":
    # ログインAPIサーバーは localhost:4000 で実行
    app.run(debug=True, port=4000)

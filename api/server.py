# encoding: utf-8
'''
パスワード管理APIサーバー

Copyright (C) 2019 yoya(@amenoyoya). All rights reserved.
GitHub: https://github.com/amenoyoya/password-manager
License: MIT License
'''
from libs.frasco import g, request, Frasco, Response
from libs.sqldb import SqlDB
import os, json

# 使用するデータベース
DATABASE = os.path.join(os.path.dirname(__file__), 'database.sqlite3')

# Flaskアプリケーション
app = Frasco(__name__)

def get_db():
    ''' Databaseのconnectionを取得 '''
    if not hasattr(g, 'databse'):
        g.database = SqlDB(DATABASE)
    return g.database

# Flaskサーバー実行
if __name__ == "__main__":
    # ログインAPIサーバーは localhost:4000 で実行
    app.run(debug=True, port=4000)

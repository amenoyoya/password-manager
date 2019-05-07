'''
データベース作成
'''

import os, sqlite3
from contextlib import closing

def fullpath(filename):
  return os.path.join(os.path.dirname(__file__), filename)

if os.path.exists(fullpath('password.db')):
  os.remove(fullpath('password.db'))

'''
パスワード・データベース
title   | username  | password
================================
タイトル | ユーザー名 | パスワード
'''
with closing(sqlite3.connect(fullpath('password.db'))) as conn:
  cursor = conn.cursor()
  cursor.execute('create table if not exists password (title text, username text, password text)')
  cursor.executemany('insert into password (title, username, password) values (?, ?, ?)', [
    ('example.com', 'admin', 'pass'),
    ('My mail address', 'mail@example.jp', 'abc123'),
    ('My bank ID', '0123456789', '0000')
  ])
  conn.commit()

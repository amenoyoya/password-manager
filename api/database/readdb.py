# encoding: utf-8
'''
パスワード管理DBからデータ読み込み
'''
import os, sqlite3, hashlib
from contextlib import closing

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

# target db file
dbfile = os.path.join(os.path.dirname(__file__), 'password.db')

with closing(sqlite3.connect(dbfile)) as conn:
    c = conn.cursor()
    # get user info
    c.execute(
        'select * from users where username = ? and password = ?;',
        ('admin', hashlib.sha256('adminpass'.encode()).hexdigest())
    )
    user = c.fetchone()
    print('login: ', user)
    
    # get user's categories
    c.execute(
        'select * from user_categories where user_id = ?;', str(user[0])
    )
    categories = c.fetchall()
    for category in categories:
        # get cotegory's password info
        c.execute(
            'select * from category_passwords where category_id = ?;', str(category[0])
        )
        passwords = [(decrypt(info[2]), decrypt(info[3]), decrypt(info[4]), decrypt(info[5])) for info in c.fetchall()]
        print(category[2], passwords)

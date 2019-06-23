# encoding: utf-8
'''
CSVファイルからパスワード管理DB作成
'''
import os, sqlite3, hashlib, random, string, csv
from contextlib import closing

# generate random string
def randomname(n):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=n))

# csv file to array
def readcsv(csvfile):
    data = []
    with open(csvfile, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            data += [[row[0], row[1], row[2], ''] if len(row) < 4 else row]
    return data

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

# delete current db file
if os.path.exists(dbfile):
    os.remove(dbfile)

# source csv files
csvfiles = {
    'サンプル': os.path.join(os.path.dirname(__file__), 'src', 'sample.csv')
}

with closing(sqlite3.connect(dbfile)) as conn:
    c = conn.cursor()
    # create table users: ユーザー情報
    c.execute('''
        create table users (id integer primary key, token varchar, username varchar, password varchar);
    ''')
    # insert values into users
    c.execute(
        'insert into users (token, username, password) values (?, ?, ?)',
        (randomname(16), 'admin', hashlib.sha256('adminpass'.encode()).hexdigest())
    )
    
    # create table user_categories: ユーザー.has_many(パスワードカテゴリー)
    c.execute('''
        create table user_categories (id integer primary key, user_id integer, category varchar);
    ''')

    # create table category_passwords: パスワードカテゴリー.has_many(パスワード情報)
    c.execute('''
        create table category_passwords (id integer primary key, category_id integer, service varchar, username varchar, password varchar, remarks text);
    ''')

    # insert values into user_categories, category_passwords
    for category, csvfile in csvfiles.items():
        # insert values into user_categories
        c.execute(
            'insert into user_categories (user_id, category) values (?, ?)',
            (1, category)
        )
        # get category id
        c.execute('select id from user_categories where category = ?', (category,))
        category_id = c.fetchone()[0]
        # insert values into category_passwords
        c.executemany(
            'insert into category_passwords (category_id, service, username, password, remarks) values (?, ?, ?, ?, ?)',
            [(category_id, encrypt(row[0]), encrypt(row[1]), encrypt(row[2]), encrypt(row[3])) for row in readcsv(csvfile)]
        )
    # commit
    conn.commit()


from flask import Flask, request
from flask_login import login_user, logout_user

# Flaskサーバーアプリケーションの作成
app = Flask(__name__)

@app.route('/login', methods=['POST'])
def login():
  try:
    if request.form['username'] == 'user' and request.form['password'] == 'password':
      login_user('user')
  except:
    response = {
      'success': False,
      'Content-Type': 'application/json',
      'data': 'Hello, world'
    }
    return flask.jsonify(response)

if __name__ == '__main__':
  # Flaskサーバー実行
  app.run()

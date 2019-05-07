from flask import Flask, request, jsonify
from flask_login import login_user, logout_user

# Flaskサーバーアプリケーションの作成
app = Flask(__name__)

@app.route('/login', methods=['POST'])
def login():
  try:
    if request.form['username'] == 'user' and request.form['password'] == 'password':
      login_user('user')
      return jsonify({
        'success': True,
        'Content-Type': 'application/json',
        'message': 'Succeeded to login'
      })
    return jsonify({
      'success': False,
      'Content-Type': 'application/json',
      'message': 'Invalid user name or password'
    })
  except:
    return jsonify({
      'success': False,
      'Content-Type': 'application/json',
      'data': 'Failed to login'
    })

if __name__ == '__main__':
  # Flaskサーバー実行
  app.run()

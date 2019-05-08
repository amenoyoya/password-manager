from flask import Flask, request, jsonify
from flask_login import UserMixin, LoginManager, login_user, logout_user, login_required

class User(UserMixin):
  def get_id(self):
    return 1

# Flaskサーバーアプリケーションの作成
app = Flask(__name__)

# セッションを使うためにシークレットキーが必要
app.secret_key = 'secret key'

login_manager = LoginManager()
login_manager.init_app(app)

# 追加
# セッションからUserを引き当てるときのコールバックです
# ここではテストなのでUser()をそのまま渡していますが、
# return User.get(user_id) などでUserの引き当てを行うものです。
@login_manager.user_loader
def load_user(user_id):
  return User()

@app.route('/login', methods=['POST'])
def login():
  if request.form['username'] == 'user' and request.form['password'] == 'password':
    login_user(User())
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

@app.route('/password', methods=['GET'])
@login_required
def password():
  return jsonify({
    'success': True,
    'Content-Type': 'application/json',
    'message': 'Succeeded to get password'
  })

if __name__ == '__main__':
  # Flaskサーバー実行
  app.run(debug=True)

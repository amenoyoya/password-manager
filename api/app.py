import flask

# Flaskサーバーアプリケーションの作成
app = flask.Flask(__name__)

@app.route('/', methods=['GET'])
def index():
  # JSONデータを返す
  response = {
    'success': False,
    'Content-Type': 'application/json',
    'data': 'Hello, world'
  }
  return flask.jsonify(response)

if __name__ == '__main__':
  # Flaskサーバー実行
  app.run()

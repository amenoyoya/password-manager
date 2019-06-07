'''
Flask RESTful API + Login Manager

@author: yoya
'''

from flask import Flask, jsonify
from flask_login import UserMixin, LoginManager, login_user, logout_user, login_required

class Resource:
  def get(self):
    return {}
  
  def post(self):
    return {}
  
  def put(self):
    return {}
  
  def delete(self):
    return {}


class User(UserMixin):
  def __init__(self, id):
    self.id = id

class Api:
  def __init__(self, app_name=__name__):
    self.app = Flask(app_name)
    self.app.config['JSON_AS_ASCII'] = False # JSONデータで日本語使用可能に
    self.login_manager = LoginManager()
    self.login_manager.init_app(self.app)

  def manage_login(self, User=User, secret_key='flask api secret key'):
    self.app.secret_key = secret_key
    
    @self.login_manager.user_loader
    def load_user(user_id):
      return User.get(user_id)

  def resource(self, Resource, route):
    resource = Resource()

    @self.app.route(route, methods=['GET'])
    def get():
      return jsonify(resource.get())
    
    @self.app.route(route, methods=['POST'])
    def post():
      return jsonify(resource.post())
    
    @self.app.route(route, methods=['PUT'])
    def put():
      return jsonify(resource.put())
    
    @self.app.route(route, methods=['DELETE'])
    def delete():
      return jsonify(resource.delete())
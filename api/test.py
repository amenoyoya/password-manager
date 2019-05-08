from flask_api import Api, Resource

class TestResource(Resource):
  def get(self):
    return {'success': True, 'message': 'Hello, world'}

if __name__ == "__main__":
  api = Api()
  api.resource(TestResource, '/')
  api.app.run(debug=True)

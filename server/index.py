# flask server to create rest api

from flask import Flask, request
from flask_restful import Resource, Api

PORT = 4000

app = Flask(__name__,static_url_path='')
api = Api(app)

class TestApi(Resource):
	def get(self):
		return "It works!"

api.add_resource(TestApi,"/")

if __name__ == "__main__":
	app.run(port=PORT)

# flask server to create rest api

from flask import Flask, request, send_from_directory

PORT = 4000

app = Flask(__name__,static_url_path='')

@app.route("/", methods=['GET'])
def home():
	return send_from_directory("static","index.html")

@app.route("/post",methods=['GET'])
def post():
	busNumber = request.args.get('busNumber')
	x = request.args.get('x')
	y = request.args.get('y')
	if ( False ): # check if request is valid here
		return "invalid", 400
	# make some sql request here on the data
	return "success" , 200

@app.route("/bus/<string:bus_id>",methods=['GET'])
def getBus():
	if ( False ): #check if valid bus id
		return "invalid", 400 
	# make sql request here
	return { "some" : "json" }, 200

@app.route("/bus",methods=['GET']) # gets all buses
def getBuses():
	return { "some" : "json", "with lots of" : "buses" }, 200

if __name__ == "__main__":
	app.run(port=PORT)

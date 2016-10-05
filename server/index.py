# flask server to create rest api

from flask import Flask, request
from flaskext.mysql import MySQL


PORT = 4000


mysql = MySQL()
app = Flask(__name__)
app.config['MYSQL_DATABASE_USER'] = 'username'
app.config['MYSQL_DATABASE_PASSWORD'] = 'password'
app.config['MYSQL_DATABASE_DB'] = 'test'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)


@app.route('/', methods=['GET'])
def home():
    return app.send_static_file('index.html')


@app.route('/bus/<string:bus_id>', methods=['GET', 'POST']) # ensure that all references to bus id are strings to support buses like 43A etc
def update_bus(bus_id=None):
    if not bus_id:
        return {'error': 'Please specify a bus_id.'}, 400

    conn = mysql.connect()
    cursor = conn.cursor()
    if request.method == 'POST':
        # TODO: check authentication here
        date = request.form['date']
        position_id = request.form['position_id']
        last_updated = datetime.datetime.now()

        sql = 'INSERT INTO `assignment` (date, bus_id, position_id, last_updated) (%s, %s, %s, %s'
        cursor.execute(sql, (date, bus_id, position_id, last_updated))
        conn.commit()
        conn.close()
        return {}, 200

    else:
        date = request.form['date']  # TODO: fix
        sql = 'SELECT * FROM `assignment` WHERE `bus_id`=%s AND `date`=%s'
        cursor.execute(sql, (bus_id, date))
        result = cursor.fetchone()
        conn.close()
        if result is None:
            return {'error': 'bus_id does not exist'}, 404
        else:
            return result, 200


@app.route('/bus', methods=['GET']) # gets all buses
def get_bus_list():
    conn = mysql.connect()
    cursor = conn.cursor()

    date = request.form['date']
    sql = 'SELECT * FROM `assignment` WHERE `date`=%s'
    cursor.execute(sql, (date,))
    result = cursor.fetchall()
    conn.close()
    return result, 200


if __name__ == "__main__":
    app.run(port=PORT)


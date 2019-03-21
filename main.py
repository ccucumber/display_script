
from influxdb import InfluxDBClient
from apscheduler.schedulers.background import BackgroundScheduler
import requests

from flask import Flask, request, jsonify
app = Flask(__name__)

host = '172.17.0.1'
#host= '192.168.90.10'
port = 8086
USER = 'root'
PASSWORD = 'root'
DBNAME = 'tutorial'
DB = InfluxDBClient(host, port, USER, PASSWORD, DBNAME)


DEVICES = ['D0','D1']


scheduler = BackgroundScheduler()


@app.route('/skorupa', methods=['POST'])
def skorupa():
    print(request)
    content = request.json
    dev_id = content['dev_id']
    dev_ip = content['IP']
    DEVICES[dev_id] = dev_ip
    print(DEVICES)
    return jsonify('')


# Influx access
def make_influx_client():
    #host = '172.17.0.1'
    host= '192.168.90.10'
    port = 8086
    USER = 'root'
    PASSWORD = 'root'
    DBNAME = 'tutorial'
    DB = InfluxDBClient(host, port, USER, PASSWORD, DBNAME)
    #DB.create_database(DBNAME)
    return DB


def tick():
    howmany = len(DEVICES)
    #print("Updating all {} the displays!".format(howmany))
    device = "in_1"
    measurement = "K3309"
    result = DB.query("SELECT {} from {} ORDER by time DESC LIMIT 1".format(device, measurement))
    #print("Result from {} : {}".format(measurement, result))
    #response = requests.post(url, json = data)


if __name__ == '__main__':
    scheduler = BackgroundScheduler()
    scheduler.add_job(tick, 'interval', seconds=10)
    scheduler.start()
    app.run(host='0.0.0.0', port=84, debug=True, use_reloader=False)


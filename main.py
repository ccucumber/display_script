import json
from influxdb import InfluxDBClient
from apscheduler.schedulers.background import BackgroundScheduler
import requests
import time
import datetime
import logging
logfl = logging.getLogger('werkzeug')
logfl.setLevel(logging.ERROR)
log = logging.getLogger()
log.setLevel(logging.INFO)

dbhost = '172.17.0.1'
#dbhost= '192.168.90.10'
port = 8086
USER = 'root'
PASSWORD = 'root'
DBNAME = 'tutorial'
DB = InfluxDBClient(dbhost, port, USER, PASSWORD, DBNAME)

from flask import Flask, request, jsonify
app = Flask(__name__)


displays={
"D9":{"machine":"K3202","number":"0","time":""},
"D7":{"machine":"K3206","number":"0","time":""},
"D8":{"machine":"K3208","number":"0","time":""},
"D4":{"machine":"K3308","number":"0","time":""},
"D5":{"machine":"K3309","number":"0","time":""},
"D1":{"machine":"K3305","number":"0","time":""},
"D3":{"machine":"K3307","number":"0","time":""},
"D10":{"machine":"K3209","number":"0","time":""},
"D2":{"machine":"K3301","number":"0","time":""},
"D6":{"machine":"Total","number":"0","time":""}
}


scheduler = BackgroundScheduler()

@app.route('/skorupa', methods=['POST', 'GET'])
def skorupa():
    #print(request)
    #print(request.headers)
    content = request.json
    dev_id = content['dev_id']
    number = ""
    try:
        last_seen = (datetime.datetime.now() - datetime.datetime.strptime(displays[dev_id]["time"], "%Y-%m-%dT%H:%M:%SZ")).total_seconds()
    
        if last_seen < 60:
            number = displays[dev_id]["number"]
    except:
        pass
    if displays[dev_id]["machine"] == "Total":
        number = displays[dev_id]["number"]
    data = {"disp" : number}
    return json.dumps(data)


def tick():

    pstr=""
    total = 0
    start = time.time()
    for display in displays.keys():
        if displays[display]["machine"] is "Total":
            number = "{:3.1f}".format(0.36*total)
            displays[display]["number"] = number
            pstr +=  "Total:" + number +";" 
            continue
	#print("Updating all {} the displays!".format(howmany))
        channel = "in_1"
        measurement = displays[display]["machine"]
        #query = f"SELECT {channel} from {measurement} ORDER by time DESC LIMIT 1"
        #query = f"SELECT LAST({channel}) from {measurement}"
        query = f"SELECT MEAN({channel}) from {measurement} WHERE time > now() - 1m"
        result = list(DB.query(query).get_points())[0]
        total += result["last"]
        number = "{:3.1f}".format(0.36*result["last"])
        displays[display]["number"] = number
        last_seen = result["time"]
        displays[display]["time"] = last_seen
        pstr +=  str(measurement) + ":" + number +"; "        
    end = time.time()
    pstr += " Time:" + "{:6.3f}".format(end - start)
    log.info(pstr)



if __name__ == '__main__':
    scheduler = BackgroundScheduler()
    scheduler.add_job(tick, 'interval', seconds=10)
    scheduler.start()
    app.run(host='0.0.0.0', port=84, debug=False, use_reloader=False)


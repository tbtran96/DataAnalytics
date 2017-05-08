from flask import Flask, render_template
from pymongo import MongoClient
from bson import json_util
import json
app = Flask(__name__)

client = MongoClient('localhost')
db = client.parking

@app.route('/')
def home():
	return render_template('home.html')

@app.route('/report', methods=['GET'])
def report():
	t0 = t1 = t2 = t3 = t4 = t5 = t6 = t7 = t8 = t9 = t10 = t11 = t12 = t13 = t14 = t15 = t16 = t17 = t18 = t19 = t20 = t21 = t22 = t23 = 0
	hours = [t0, t1, t2, t3, t4, t5, t6, t7, t8, t9, t10, t11, t12, t13, t14, t15, t16, t17, t18, t19, t20, t21, t22, t23]
	try:
		q = db.vacancyChanges.find()
	except Exception as e:
		return str(e)
	for parkingSpot in q:
		timestamp = str(parkingSpot['_id'].generation_time)
		hour = int(timestamp[11] + timestamp[12])

		if (parkingSpot['vacant'] == 'False'):
			for it in range (hour, 24):
				hours[it] = hours[it] + 1
		elif (parkingSpot['vacant'] == 'True'):
			for it in range (hour+1, 24):
				if (hours[it] > 0):
					hours[it] = hours[it] - 1
			
		print(timestamp)
		print(parkingSpot['vacant'])
		t0 = hours[0]
		t1 = hours[1]
		t2 = hours[2]
		t3 = hours[3]
		t4 = hours[4]
		t5 = hours[5]
		t6 = hours[6]
		t7 = hours[7]
		t8 = hours[8]
		t9 = hours[9]
		t10 = hours[10]
		t11 = hours[11]
		t12 = hours[12]
		t13 = hours[13]
		t14 = hours[14]
		t15 = hours[15]
		t16 = hours[16]
		t17 = hours[17]
		t18 = hours[18]
		t19 = hours[19]
		t20 = hours[20]
		t21 = hours[21]
		t22 = hours[22]
		t23 = hours[23]



	return render_template('report.html', t0=t0, t1=t1, t2=t2, t3=t3, t4=t4, t5=t5, t6=t6, t7=t7, t8=t8, t9=t9, t10=t10, t11=t11, t12=t12, t13=t13, t14=t14, t15=t15, t16=t16, t17=t17, t18=t18, t19=t19, t20=t20, t21=t21, t22=t22, t23=t23)

@app.route('/getAllParkingData', methods=['GET'])
def getAllParkingData():
	try:
		q = db.vacancyChanges.find()
	except Exception as e:
		return str(e)
	return json.dumps(list(q), default=json_util.default)

@app.route('/currentParkingStatus', methods=['GET'])
def getAllCurrentParkingStatus():
	try:
		q = db.vacancyChanges.aggregate(
			[
				{"$sort": {"_id": -1}}, 
				{"$group": 
					{"_id":"$parkingId", 
					"latestTimeStamp":{"$max": "$_id"}, 
					"currentStatus": { "$first": "$$ROOT"} 
					} 
				}
			]
		)

		vacancyList = []
		for parkingSpot in q:
			vacancyData = {
				'id' : parkingSpot['_id'],
				'vacant' : parkingSpot['currentStatus']['vacant'],
				'ts' : parkingSpot['currentStatus']['_id'].generation_time
			}
			vacancyList.append(vacancyData)
	except Exception as e:
		return str(e)
	return json.dumps(vacancyList, default=json_util.default)


@app.route('/index/')
def index():
	return 'Index Page. Try the hello page out.'

@app.route('/hello/')
@app.route('/hello/<name>')
def hello_world(name=None):
	return render_template('hello.html', name=name)

if __name__ == '__main__':
	app.run()

'''

Algorithm:-----
1) Fetch the latest sensor value from the device.

2) Store the sensor value in a list(History_data), that will be used for computing z-score.

3) Compute the z-score and upper and lower threshold bounds for normal and anomalous readings.

4) Check if the sensor reading is within the range for normal readings.

5) If it is not in range, Turn on sound Buzzer.

6) Wait for 11 seconds.

7) Repeat from step 1.

'''
import conf,json,time,math,statistics
from boltiot import Bolt

def compute_bounds(history_data,frame_size,factor):
	if len(history_data)<frame_size:
		return None
	#if there is no historical data to compute threshold band,return None
	if len(history_data)>frame_size:
		del history_data[0:len(history_data)-frame_size]
	#most recent 6 sensor_value is taken as history_data

	Mn=statistics.mean(history_data)
	#calculating average
	variance=0
	for data in history_data:
		variance+=math.pow((data-Mn),2)
	zn=factor*math.sqrt(variance/frame_size)
	High_bound=history_data[frame_size-1]+zn
	Low_bound=history_data[frame_size-1]-zn
	return [High_bound+6,Low_bound-6]

#print(compute_bounds([200,200,200,200,200,200],conf.FRAME_SIZE,conf.MUL_FACTOR))	#TESTING phase

mybolt=Bolt(conf.API_KEY,conf.DEVICE_ID)#unique device id as well as cloud api_key
history_data=[]

while True:
	response=mybolt.analogRead('A0')
	#sensor data collected in object response is in UTF-8 (text format)
	data=json.loads(response)
	#with the help of (JavaScript Object Notation) parsing the data to dict
	if data['success']!=1:
		print("There was an error while retriving the data.")
		print("This is the error:"+data['value'])
		time.sleep(11)
		continue

	sensor_value=0
	try:
		sensor_value=int(data['value'])
		#sensor_value=int(sensor_value/10)#if your are using temperature sensor
		print("This is the value",sensor_value)
	except e:
		print("There was an error while parsing the response:",e)
		continue
	#calculating z score= used to determine outlier
	bound=compute_bounds(history_data,conf.FRAME_SIZE,conf.MUL_FACTOR)
	#argument= compute_bounds(environment_data collected,Buffer size(bucket),constant numeric factor(bound size))
	
	if not bound:
		required_data_count=conf.FRAME_SIZE-len(history_data)
		print("Not enough data to compute z-score. Need",required_data_count,"more data points.")
		history_data.append(sensor_value)
		time.sleep(11)
		continue
	try:
		print("High and Low bound: ",bound)
		#if our live sensor value does not lies in bound,Hello IOT, notify the bosss(Intrusion Detected).
		if sensor_value > bound[0] or sensor_value < bound[1]:
			mybolt.digitalWrite('1','HIGH')
			print("Anomaly Detected")
			#print(response)
		else:
			#If no fluctuation in sensor value, turn of your buzzer.
			mybolt.digitalWrite('1','LOW')
			print("Normal Environment")
		history_data.append(sensor_value)
	except Exception as e:
		print("Error",e)
	time.sleep(11)


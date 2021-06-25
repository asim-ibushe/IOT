from boltiot import Bolt
import time
import json
api_key="26a1f099-9088-4bfa-b7a4-a3b5c5048cdb"
device_id="BOLT3847612"
mybolt = Bolt(api_key, device_id)
while True:
	light=mybolt.analogRead("A0")
	print(light)
	data=json.loads(light)
	num=int(data["value"])
	if num<30:
		response = mybolt.digitalWrite('0', 'HIGH')
		print(response)
	elif num>100:
		response = mybolt.digitalWrite('0', 'LOW')
		print(response)
	time.sleep(7)


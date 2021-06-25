from boltiot import Bolt
api_key="26a1f099-9088-4bfa-b7a4-a3b5c5048cdb"
device_id="BOLT3847612"
mybolt=Bolt(api_key,device_id)
print(type(mybolt))
response = mybolt.isOnline()
print(type(response))
print (response)

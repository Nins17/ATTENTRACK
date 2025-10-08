# Una pip install requests
import requests

BASE_URL = 'https://api.textbee.dev/api/v1'
API_KEY = 'd9f24a38-b31f-4930-9c3c-ebfac749f9ac'
DEVICE_ID = '68e5fdabc2046740cec292e6'



#Notification
Number = '09278826869' #fetch number of guardian here starts with 0
Name= 'Richard' #fetch student name here
Time= '9:00' #fetch time attendance was taken
AttendanceNotif = requests.post(
  
    f'{BASE_URL}/gateway/devices/{DEVICE_ID}/send-sms',
    json={
        'recipients': [f'+{Number}'],  \
        'message': f'{Name} was marked present at {Time}.'
    },
    headers={'x-api-key': API_KEY}
)

print(AttendanceNotif.json())

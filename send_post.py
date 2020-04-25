import requests
from datetime import datetime

# data to be sent to api 
API_ENDPOINT = 'http://127.0.0.1:5000/update-loc'
data = {'user_id':'Chirag1234', 
        'latitude':"10.234", 
        'longitude':"10.234", 
        'time_stamp': str(datetime.now()) } 
  
# sending post request and saving response as response object 
r = requests.post(url = API_ENDPOINT, data = data) 
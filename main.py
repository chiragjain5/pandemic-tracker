from flask import render_template
from flask import request

from flask import Flask
import pymysql
import datetime
from datetime import datetime
import sys
app = Flask(__name__)


@app.route("/update-loc",methods=["GET","POST"])  # accept a post request
def update_usr_loc():
   
    user_id = request.form['user_id']  #run send_post.py to get the post request
    lati = request.form['latitude']
                   
    longi = request.form['longitude']
    time_stamp = request.form['time_stamp']

    connection = pymysql.connect(host="127.0.0.1",
                                 user="root",
                                 password="ccl_proj2",
                                 db="pandemic_tracker")

    with connection:
        cur = connection.cursor()
        
        cur.execute("DROP TABLE user_loc_time;")

        cur.execute(
            "CREATE TABLE IF NOT EXISTS user_loc_time ( user_id CHAR(100) , latitude DECIMAL(12,9), longitude DECIMAL(12,9), time_stamp timestamp );")

        cur.execute(
            "Insert into user_loc_time (user_id, latitude, longitude,time_stamp) VALUES ('%s','%s','%s', '%s')"% (user_id, lati, longi, time_stamp))
            
     
        cur.execute("Select * from user_loc_time;")
    
    print(cur.fetchall(),file=sys.stderr)

    return render_template('template.html')
            
if __name__ == "__main__":
    app.run(debug=True)

            
            
            
            
            
            
            
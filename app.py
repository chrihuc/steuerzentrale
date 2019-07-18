# -*- coding: utf-8 -*-
"""
Created on Thu Jul 18 18:13:08 2019

@author: hc
"""
from flask import Flask, render_template, request
from outputs.mqtt_publish import mqtt_pub

app = Flask(__name__)


@app.route("/", methods=['GET', 'POST'])
def index():
    print(request.method)
    if request.method == 'POST':
        if request.form.get('Besucher') == 'Wir sind Besucher':
            # pass
            print("Besucher")
            command = {'Szene':'Besuch'}
            mqtt_pub("Command/Szene/Besuch", command)
        elif  request.form.get('AlarmAus') == 'Alarmanlage aus':
            # pass # do something else
            print("AlarmAus")
            command = {'Szene':'AlarmanlageAus'}
            mqtt_pub("Command/Szene/AlarmanlageAus", command)            
        elif  request.form.get('AlarmEin') == 'Alarmanlage ein':
            # pass # do something else
            print("AlarmEin") 
            command = {'Szene':'AlarmanlageEin'}
            mqtt_pub("Command/Szene/AlarmanlageEin", command)  
        else:
            # pass # unknown
            return render_template("hello.html")
    elif request.method == 'GET':
        # return render_template("index.html")
        print("No Post Back Call")
    return render_template("hello.html")

def main():
    app.run(host='0.0.0.0', port=5555)

if __name__ == '__main__':
    main()
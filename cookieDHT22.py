#! /usr/bin/env python
import pigpio
import DHT22
import tweepy
from time import sleep
from datetime import datetime
import sqlite3

conn = sqlite3.connect('tweepy.db')
c = conn.cursor()

API_KEY = '0czHGLaaOx4wkcR0SsPxUYGeZ'
API_SECRET = 'XiIlziEeaRIuTl8CYoejy00DuFO2AAemu2wKLsVUjXDht8jLku '
ACCESS_TOKEN = '792094452776972289-FAEZpkgosa6rq2d6NTSUqVBE3R4cgas'
ACCESS_TOKEN_SECRET = 'vWxytTUJ0IVYj3hL9BnTd5ziz8yZIQo8bVSxTXAGTTT8t '

auth = tweepy.OAuthHandler(API_KEY, API_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)

#Initiate GPIO for pigpio
pi=pigpio.pi()
#Setup the sensor
dht22=DHT22.sensor(pi, 4)   #use the actual GPIO pin name
dht22.trigger()  #grab the first junk reading

sleepTime=3     #should be above 2 second
SlpTime=120

def readDHT22() :
    dht22.trigger()
    humidity = '%.2f' % (dht22.humidity())
    temp = '%.2f' % (dht22.temperature())
    return (humidity,temp)

while 1:
	TEMP1,TEMP2 = readDHT22()
	sleep(sleepTime)
	TEMP1,TEMP2 =readDHT22()
	sleep(sleepTime)

	humidity,temperature = readDHT22()
	print("Humidity is : " +humidity + "%")
	print("Temperature is: " + temperature + "C")
	thetime = datetime.now().strftime('%-I:%M%P on %d-%m-%Y')
	sleep(sleepTime)

	humidity = float(humidity)
	temperature = float(temperature)

	if humidity > 60.00 and humidity < 70.00:
		h="Humidity is good"
	elif humidity < 60.00:
		h="Humidity is low"
	elif humidity > 70.00:
		h="Humidity is high"

	if temperature > 16.00 and temperature < 22.00:
		t="Temperature is good for fertilisation"
	elif temperature > 20.00 and temperature < 35.00:
		t="Temperature is good for harvest"
	elif temperature < 16.00:
		t="Temp too low"
	elif temperature > 35.00:
		t="Temp too high"

	humidity = str(humidity)
	temperature = str(temperature)
	print(h)
	print(t)
	c.execute("INSERT INTO analysis(date, temp, condition1, humidity, condition2) VALUES (?,?,?,?,?)",(thetime,temperature,t,humidity,h))
	api.update_status("Temperature: "+temperature +"C "+t+"\n"+"Humidity: "+humidity+"% "+h+" at "+thetime)
	conn.commit()
	sleep(SlpTime)

conn.close()  



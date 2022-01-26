import RPi.GPIO as GPIO
import time
import socket

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)



# create a socket object
serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# get local machine name
host = 'Server's IP Addrsse'

port = 9999
serversocket.bind((host, port))
serversocket.listen(5)

clientsocket, addr = serversocket.accept()

print("Got a connection from %s" % str(addr))



TRIG = 17
ECHO = 27
LED = 18
Motion = 23

print("Distance Measureement")
print ("Motion Sensor IS Active!!")
GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO,GPIO.IN)
GPIO.setup(LED,GPIO.OUT)
GPIO.setup(Motion,GPIO.IN)

while True:
   
    signal  = GPIO.input(Motion)
    if signal == 0:
        print("__")
        GPIO.output(LED,0)
        time.sleep(1)
        msg = "__\r\n"
        clientsocket.send(msg.encode('UTF-8'))
       
       
    elif signal == 1:
        print("Motion has been detected!!")
        GPIO.output(LED,1)
        time.sleep(1)
        GPIO.output(TRIG,False)
        time.sleep(1)
       
        GPIO.output(TRIG ,True)
        time.sleep(0.00001)
        GPIO.output(TRIG,False)
       
        while GPIO.input(ECHO)==0:
            Pulse_start = time.time()
       
        while GPIO.input(ECHO)==1:
            Pulse_end = time.time()
       
        Pulse_duration = Pulse_end - Pulse_start
       
        distance  = Pulse_duration * 17150
       
        distance = round(distance, 2)
       
        print ("distance = ", distance, "cm")
        
        msg2 = "Motion has been detected!!\n distance = " + str(distance) + " cm" 
        clientsocket.send(msg2.encode('UTF-8'))
       
   
GPIO.cleanup()

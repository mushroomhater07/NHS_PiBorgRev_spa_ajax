#Modified by smartbuilds.io
#Date: 27.09.20
#Desc: This web application serves a motion JPEG stream
##############################################################
import PicoBorgRev3 as PicoBorgRev
voltageIn = 12.0
voltageOut = 6.0

if voltageOut > voltageIn:
    maxPower = 1.0
else:
    maxPower = voltageOut / float(voltageIn)
PicoBorgRev.ScanForPicoBorgReverse()
PBR = PicoBorgRev.PicoBorgRev()
PBR.Init()
PBR.ResetEpo()
PBR.MotorsOff()

print (PBR.busNumber)        # Reading parameters (after Init)           # Shows which I²C bus the board is connected on
print (PBR.foundChip)                  # See if the board is found / not found
maxPower = 21;
powerpercent = maxPower;
# website  
def for1():
    print("forward", powerpercent)
    # PBR.SetMotor1(+powerpercent)
    # PBR.SetMotor2(+powerpercent)

def back():
    print("backward", powerpercent)
    # PBR.SetMotor1(-powerpercent)
    # PBR.SetMotor2(-powerpercent)

def right():
    print("clockwise", powerpercent)
    # PBR.SetMotor1(+powerpercent)
    # PBR.SetMotor2(-powerpercent)

def left():
    print("anti-clockwise", powerpercent)
    # PBR.SetMotor1(-powerpercent)
    # PBR.SetMotor2(+powerpercent)

def stop():
    print("stop")
    # PBR.MotorsOff()
def changespeed(haha):
    global powerpercent, maxPower;
    powerpercent = maxPower * int(haha) /100
    print(powerpercent, maxPower);
    

##############################################################
# main.py
# import the necessary packages
from flask import Flask, render_template, Response, request, send_from_directory
from camera import VideoCamera
import os

pi_camera = VideoCamera(flip=False) # flip pi camera if upside down.

# App Globals (do not edit)
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html') #you can customze index.html here

def gen(camera):
    #get camera frame
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(gen(pi_camera),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

# Take a photo when pressing camera button
@app.route('/picture')
def take_picture():
    pi_camera.take_picture()
    return "None"

#hey lau define post receive
@app.route('/work', methods=['POST'])
def post():
    if request.method == "POST":
        mode = request.form["mode"]
        match mode:
            case "Forward":
                for1()
            case "Backward":
                back()
            case "Clockwise":
                right()
            case "Anti-clockwise":
                left()
            case "Handbrake":
                stop()
    return mode

@app.route('/sped', methods=['POST'])
def posto():
    if request.method == "POST":
        mode = request.form["speed"];
        changespeed(mode);
    return mode

if __name__ == '__main__':
    app.run(host='0.0.0.0',port="80", debug=False)

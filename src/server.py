from flask import Flask, render_template, send_file, send_from_directory, request
import cv2
import base64
import os
from worker import Worker
import time
import sys
from credentials import guard
#from gpiozero import CPUTemperature

print (sys.version)

os.environ['TZ'] = 'Europe/Eastern'
time.tzset()

app = Flask(__name__)
worker = Worker()
self_path = os.path.dirname(os.path.realpath(__file__))

@app.route('/')
def index():
    #if not guard(request):
    #    return send_file(self_path + '/../resources/html/login.html')
    #return send_file(self_path + '/../resources/html/index.html')
    return send_file(self_path + '/static/index.html')

@app.route('/feed')
def send_feed():
    if not guard(request):
        return 'ERROR'

    worker.frame_access.acquire()

    encoded = ""

    if worker.frame_base64 is not None:
        encoded = worker.frame_base64

    worker.frame_access.release()

    return encoded


@app.route('/altered')
def send_altered():
    if not guard(request):
        return 'ERROR'

    worker.altered_access.acquire()

    encoded = ""

    if worker.altered_base64 is not None:
        encoded = worker.altered_base64

    worker.altered_access.release()

    return encoded


@app.route('/movement')
def send_movement_factor():
    if not guard(request):
        return 'ERROR'

    worker.movement_factor_access.acquire()

    number = worker.movement_factor
    active = worker.movement_active

    worker.movement_factor_access.release()

    return {
        "factor": str(number),
        "active": str(1) if active else str(0)
    }


@app.route('/movement-active')
def send_movement_active():
    if not guard(request):
        return 'ERROR'

    worker.movement_factor_access.acquire()

    active = worker.movement_active

    worker.movement_factor_access.release()

    if active:
        return str(1)
    else:
        return str(0)


@app.route('/login')
def login():
    if not guard(request):
        return "0"

    return "1"

@app.route('/get-active')
def get_active():
    if not guard(request):
        return 'ERROR'

    worker.active_access.acquire()

    active = worker.active

    worker.active_access.release()

    if active:
        return str(1)
    else:
        return str(0)

@app.route('/toggle-active')
def toggle_active():
    if not guard(request):
        return 'ERROR'

    worker.active_access.acquire()

    worker.active = not worker.active

    worker.active_access.release()

@app.route('/get-info')
def get_info():
    if not guard(request):
        return 'ERROR'

    result = ''
    stream = os.popen('bash ' + self_path + '/shell/memory.sh')
    output = stream.read()
    result += 'Memoria: ' + output

    stream = os.popen('bash ' + self_path + '/shell/gpu.sh')
    output = stream.read()
    result += '; GPU: ' + output

    f = open("/sys/class/thermal/thermal_zone0/temp")
    t = f.read()

    result += '; Temperatura: ' + str(int(int(t)/1000)) + '.' + str(int(int(t) % 1000)) + '° C'

    return result

@app.route('/<path:path>')
def send_js(path):
    return send_from_directory('static', path)


worker.run()

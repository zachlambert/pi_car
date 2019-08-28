
import time

from flask import render_template, Response

from app import app
from run import control_queue, display_queue, message_queue


@app.route("/")
@app.route("/index")
def index():
    control_queue.put("start_program_none")
    return render_template("index.html")    
    
@app.route("/display")
def display():
    def frame_generator():
        while True:
            time.sleep(0.05) #20 fps at most
            encoded_bytes = display_queue.get()
            yield (b'--frame\r\n' +
                   b'Content-Type: image/jpeg\r\n\r\n' +
                   encoded_bytes +
                   b'\r\n')
    return Response(frame_generator(),
                    mimetype="multipart/x-mixed-replace; boundary=frame")
    

@app.route("/control/<control_name>")
def control(control_name):
    message_queue.put("Received: {}".format(control_name))
    control_queue.put(control_name)
    return Response("queued")


@app.route("/manual")
def manual():
    control_queue.put("start_program_manual")
    return render_template("manual.html")

@app.route("/line_follower")
def line_follower():
    control_queue.put("start_program_line_follower")
    return render_template("line_follower.html")

@app.route("/test")
def test():
    control_queue.put("start_program_test")
    return render_template("test.html")


from multiprocessing import Queue
import time

from flask import Flask, render_template, Response


app = Flask(__name__)
image_queue = Queue(maxsize=2)
        

def put_image(encoded_bytes):
    if image_queue.empty():
        image_queue.put(encoded_bytes)

def frame_generator():
    while True:
        # at most 20 fps
        time.sleep(0.05)
        encoded_bytes = image_queue.get()
        yield (b'--frame\r\n' +
               b'Content-Type: image/jpeg\r\n\r\n' +
               encoded_bytes +
               b'\r\n')       

@app.route("/")
def index():
    return render_template("template.html")

        
@app.route("/display")
def display():
    return Response(frame_generator(),
                    mimetype="multipart/x-mixed-replace; boundary=frame")
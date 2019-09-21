
from flask import Flask, render_template, Response


app = Flask(__name__)
frame_generator = None

@app.route("/")
def index():
    return render_template("template.html")

        
@app.route("/display")
def display():
    return Response(frame_generator(),
                    mimetype="multipart/x-mixed-replace; boundary=frame")
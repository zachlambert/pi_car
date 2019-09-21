
from multiprocessing import Process
import time

from picamera.array import PiRGBArray
from picamera import PiCamera
import numpy as np
import cv2


_CAMERA_SIZE = (320, 240)
_ENCODE_PARAMS = [int(cv2.IMWRITE_JPEG_QUALITY), 90]

def _get_encoded_bytes_for_frame(frame):
    result, encoded_image = cv2.imencode(".jpg", frame, _ENCODE_PARAMS)
    return encoded_image.tostring()

class Camera:
    
    def __init__(self):
        self._camera = PiCamera()
        self._camera.resolution = _CAMERA_SIZE
        self._camera.rotation = 180
        self._process = None
        
    def start_server(self):
        from camera.app import app
        self._process = Process(target=app.run, args={ 'debug':True, 'port':5000})
        time.sleep(0.1) # Esnure the camera has had 0.1 seconds to initialise
        self._process.start()
    
    def stop_server(self):
        if self._process != None:
            self._process.terminate()
            self._process = None
            
    def frame_generator(self):                
        for frame in self._camera_stream():
            encoded_bytes = _get_encoded_bytes_for_frame(frame)
            yield (b'--frame\r\n' +
                   b'Content-Type: image/jpeg\r\n\r\n' +
                   encoded_bytes +
                   b'\r\n')
        
    def _camera_stream(self):
        image_storage = PiRGBArray(self._camera, size=self._camera.resolution)
        camera_stream = self._camera.capture_continuous(
            image_storage, format="bgr", use_video_port=True)
        
        for raw_frame in camera_stream:
            yield raw_frame.array
            image_storage.truncate(0)
                                             

def test_camera():
    camera = Camera()
    camera.start_server()
    user_input = ""
    while user_input!="stop":
        print("Type 'stop' to stop the program.")
        user_input = input(">")
    camera.stop_server()
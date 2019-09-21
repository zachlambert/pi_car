
from multiprocessing import Process
import time

from picamera.array import PiRGBArray
from picamera import PiCamera
import cv2

from camera import app
from utils.updater import Updater


_CAMERA_SIZE = (320, 240)
_ENCODE_PARAMS = [int(cv2.IMWRITE_JPEG_QUALITY), 90]
server_started = False

def _encode_frame(frame):
    result, encoded_image = cv2.imencode(".jpg", frame, _ENCODE_PARAMS)
    return encoded_image.tostring()


class Camera:
    
    def __init__(self):
        camera = PiCamera()
        camera.resolution = _CAMERA_SIZE
        camera.rotation = 180
    
        time.sleep(0.1)

        self._image_storage = PiRGBArray(camera, size=camera.resolution)
        self._camera_stream = camera.capture_continuous(
            self._image_storage, format="bgr", use_video_port=True)
    
    def update(self):
        raw_frame = next(self._camera_stream)
        frame = raw_frame.array
        if server_started:
            encoded_bytes = _encode_frame(frame)
            app.put_image(encoded_bytes)
        self._image_storage.truncate(0)
        return frame


def start_server():
    global server_started
    server_process = Process(
        target=app.app.run, kwargs={ 'host':'0.0.0.0', 'port':5001})
    server_process.start()
    server_started = True
    return server_process


def test():
    server_process = start_server()
    camera = Camera()
    
    def update(time):
        frame = camera.update()
        print("Received frame of shape ", frame.shape)
    
    updater = Updater(0.01)
    updater.add(update)
    while updater.timer<120:
        updater.update()

    server_process.terminate()
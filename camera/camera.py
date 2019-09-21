
from multiprocessing import Process
import time

from picamera.array import PiRGBArray
from picamera import PiCamera
import cv2
import numpy as np

from camera import app
from utils.updater import Updater


_CAMERA_SIZE = (320, 240)
_ENCODE_PARAMS = [int(cv2.IMWRITE_JPEG_QUALITY), 90]

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
        self._image_storage.truncate(0)
        return frame


class CameraServer:
    
    def __init__(self):
        self._server_process = Process(
                target=app.app.run, kwargs={ 'host':'0.0.0.0', 'port':5001})
        self._server_process.start()

    def stop(self):
        self._server_process.terminate()
        
    def put_images(self, *frames):
        rgb_frames = []
        for frame in frames:
            if len(frame.shape)==2:
                rgb_frames.append(cv2.cvtColor(frame, cv2.COLOR_GRAY2BGR))
            else:
                rgb_frames.append(frame)
                                  
        combined_frame = np.concatenate(rgb_frames, axis=0)
        encoded_bytes = _encode_frame(combined_frame)
        app.put_image(encoded_bytes)


def test():
    server = CameraServer()
    camera = Camera()
    
    def update(time):
        frame = camera.update()
        server.put_images(frame)
    
    updater = Updater(0.01)
    updater.add(update)
    while updater.timer<120:
        updater.update()

    server.stop()

import time
import importlib

from run import display_queue, control_queue

program = None


def put_output_image(encoded_bytes):
    if display_queue.empty():
        display_queue.put(encoded_bytes)
    
def read_instructions():
    global program
    while not control_queue.empty():
        instruction = control_queue.get()
        if instruction.find("start_program")==0:
            if program!=None:
                program.stop()
            program = None
            if instruction=="start_program_manual":
                program = importlib.import_module('programs.manual').Program()
            elif instruction=="start_program_line_follower":
                program = importlib.import_module('programs.line_follower_program').Program()
            elif instruction=="start_program_test":
                program = importlib.import_module('programs.test').Program()
        else:
            if program!=None:
                program.update(instruction)
        
    time.sleep(0.01)
    
def start(stream_video=False):
    if stream_video:
        from camera import pi_camera_stream
        
        camera = pi_camera_stream.setup_camera()
        time.sleep(0.1) # Allow camera to setup
        for frame in pi_camera_stream.start_stream(camera):
            encoded_bytes = pi_camera_stream.get_encoded_bytes_for_frame(frame)
            put_output_image(encoded_bytes)
            read_instructions()
    else:
        while True:
            read_instructions()
    
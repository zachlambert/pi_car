# -*- coding: utf-8 -*-

from multiprocessing import Process

from run import control_queue, message_queue, handler


def cmd_input():
    while True:
        user_input = input(">")
        control_queue.put(user_input)
        
def cmd_output():
    while True:
        while not message_queue.empty():
            print(message_queue.get())
        
        
def app_input():
    #app_process = Process(target=app.run, kwargs={"host":"0.0.0.0", "port":5001})
    app.run(host="0.0.0.0", port=5001)
    
        
def app_output():
    while True:
        while not message_queue.empty():
            message = message_queue.get()
            print(message) #temporary
            #Todo: print message to webpage
            
            
print("Type 'app' or 'cmd' for input method")
input_func = None
output_func = None
valid = False
stream_video = False
while not valid:
    user_input = input(">")
    if user_input=="app":
        input_func = app_input
        output_func = app_output
        valid = True
        stream_video = True
        
        from app import app
        
    elif user_input=="cmd":
        input_func = cmd_input
        output_func = cmd_output
        valid = True
    

output_process = Process(target=output_func)
output_process.start()
    
handler_process = Process(target=handler.start, args=(stream_video,))
handler_process.start()

input_func()

from actuation.motors import testMotors, testEncoders
from actuation.smart_motors import testSmartMotors
from actuation.servos import testServos
from sensors.compass import testCompass
from sensors.opto_interrupter import testOptoInterrupter

test_strings = ["motors", "encoders", "servos", "smart_motor", "compass", "opto_interrupter"]
test_functions = [testMotors, testEncoders, testServos, testSmartMotors, testCompass, testOptoInterrupter]

running = True

while running:

    print("Enter name of component to test or type 'exit'")    
    user_input = input(">").strip()
    
    found = False
    
    i = 0
    while i < len(test_strings):
        if test_strings[i] == user_input:
            found=True
            break
        i+=1
        
    if found:
        print("Running test program for ", test_strings[i])
        print("")
        test_functions[i]()
        print("")
    elif user_input == "exit":
        running = False
        print("Exiting")
    else: 
        print("Invalid input")
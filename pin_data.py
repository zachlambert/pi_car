
class MotorPins:
    
    def __init__(self, IN1, IN2, EN):
        self.IN1 = IN1
        self.IN2 = IN2
        self.EN = EN
        
    def flip_direction(self):
        prev_IN1 = self.IN1
        self.IN1 = self.IN2
        self.IN2 = prev_IN1
        
        
class EncoderPins:
    
    def __init__(self, OUT):
        self.OUT = OUT
        
        
class OptoInterrupterPins:
    
    def __init__(self, OUT):
        self.OUT = OUT
        
        
class ServoPins:
    
    def __init__(self, PWM):
        self.PWM = PWM
    
    
class CarPins:
    
    def __init__(self, left_motor_pins, right_motor_pins, left_encoder_pins, right_encoder_pins):
        self.left_motor_pins = left_motor_pins
        self.right_motor_pins = right_motor_pins
        self.left_encoder_pins = left_encoder_pins
        self.right_encoder_pins = right_encoder_pins
    
    
def get_pins():
    pins = {
        "left motor": MotorPins(11, 13,15),
        "right motor": MotorPins(22, 24, 26),
        "left encoder": EncoderPins(7),
        "right encoder": EncoderPins(8),
        "pan servo": ServoPins(10),
        "tilt servo": ServoPins(12),
        "left opto-interrupter": OptoInterrupterPins(16),
        "right opto-interrupter": OptoInterrupterPins(18),
    }
    pins["car"] = CarPins(pins["left motor"], pins["right motor"], pins["left encoder"], pins["right encoder"])    
    
    return pins
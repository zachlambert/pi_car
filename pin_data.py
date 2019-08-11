
class _MotorPins:
    
    def __init__(self, IN1, IN2, EN):
        self.IN1 = IN1
        self.IN2 = IN2
        self.EN = EN
        
    def flip_direction(self):
        prev_IN1 = self.IN1
        self.IN1 = self.IN2
        self.IN2 = prev_IN1
        
        
class _EncoderPins:
    
    def __init__(self, OUT):
        self.OUT = OUT
        
        
class _OptoInterrupterPins:
    
    def __init__(self, OUT):
        self.OUT = OUT
        
        
class _ServoPins:
    
    def __init__(self, PWM):
        self.PWM = PWM
    
    
class _CarPins:
    
    def __init__(self, left_motor_pins, right_motor_pins,
                 left_encoder_pins, right_encoder_pins):
        self.left_motor_pins = left_motor_pins
        self.right_motor_pins = right_motor_pins
        self.left_encoder_pins = left_encoder_pins
        self.right_encoder_pins = right_encoder_pins
    
    
class _LineFollowerPins:
    
    def __init__(self, car_pins,
                 left_opto_interrupter_pins, right_opto_interrupter_pins):
        self.car_pins = car_pins
        self.left_opto_interrupter_pins = left_opto_interrupter_pins
        self.right_opto_interrupter_pins = right_opto_interrupter_pins
        
    
def get_pins():
    pins = {
        "left motor": _MotorPins(11, 13, 15),
        "right motor": _MotorPins(22, 24, 26),
        "left encoder": _EncoderPins(7),
        "right encoder": _EncoderPins(8),
        "pan servo": _ServoPins(15), #BCM
        "tilt servo": _ServoPins(18), #BCM
        "left opto-interrupter": _OptoInterrupterPins(16),
        "right opto-interrupter": _OptoInterrupterPins(18),
    }
    pins["car"] = _CarPins(
        pins["left motor"], pins["right motor"],
        pins["left encoder"], pins["right encoder"])    
    pins["line follower"] = _LineFollowerPins(
        pins["car"],
        pins["left opto-interrupter"], pins["right opto-interrupter"])
        
    return pins
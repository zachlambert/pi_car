

class MotorPins:
    
    def __init__(self, IN1, IN2, EN):
        self.IN1 = IN1
        self.IN2 = IN2
        self.EN = EN
        
    def flipDirection(self):
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
        
def getPins():
    
    pins = {
        "left motor": MotorPins(11, 13,15),
        "right motor": MotorPins(22, 24, 26),
        "left encoder": EncoderPins(7),
        "right encoder": EncoderPins(8),
        "pan servo": ServoPins(10),
        "tilt servo": ServoPins(12),
        "left opto-interrupter": OptoInterrupterPins(16),
        "right opto-interrupter": OptoInterrupterPins(18)
    }
    
    return pins
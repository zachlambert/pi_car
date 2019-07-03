from gpiozero import DigitalInputDevice, DigitalOutputDevice, PWMOutputDevice

print("Starting robot car program.")

#Pins

HW95_IN1_PIN = "BCM17"
HW95_IN2_PIN = "BCM21"
HW95_ENA_PIN = "BCM22"
HW95_IN3_PIN = "BCM10"
HW95_IN4_PIN = "BCM9"
HW95_ENB_PIN = "BCM11"

#Motor Driver

hw95_in1 = DigitalOutputDevice(HW95_IN1_PIN)
hw95_in2 = DigitalOutputDevice(HW95_IN2_PIN)
hw95_enA = PWMOutputDevice(HW95_ENA_PIN)

hw95_in3 = DigitalOutputDevice(HW95_IN3_PIN)
hw95_in4 = DigitalOutputDevice(HW95_IN4_PIN)
hw95_enB = PWMOutputDevice(HW95_ENB_PIN)

hw95_in1.value = True
hw95_in2.value = False
hw95_enA.value = 0.5
hw95_enA.on()


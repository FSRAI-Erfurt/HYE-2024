import RPi.GPIO as GPIO

class MotorController:
    def __init__(self, enable_a, in1_a, in2_a, enable_b, in1_b, in2_b):
        self.enable_a = enable_a
        self.in1_a = in1_a
        self.in2_a = in2_a
        self.enable_b = enable_b
        self.in1_b = in1_b
        self.in2_b = in2_b
        
        GPIO.setmode(GPIO.BOARD)
        
        GPIO.setup(self.enable_a, GPIO.OUT)
        GPIO.setup(self.in1_a, GPIO.OUT)
        GPIO.setup(self.in2_a, GPIO.OUT)
        GPIO.setup(self.enable_b, GPIO.OUT)
        GPIO.setup(self.in1_b, GPIO.OUT)
        GPIO.setup(self.in2_b, GPIO.OUT)
        
        self.pwm_a = GPIO.PWM(self.enable_a, 1000)
        self.pwm_b = GPIO.PWM(self.enable_b, 1000)
        
        self.pwm_a.start(0)
        self.pwm_b.start(0)
        
    def set_motor_a(self, speed, direction):
        GPIO.output(self.in1_a, direction == "forward")
        GPIO.output(self.in2_a, direction == "backward")
        self.pwm_a.ChangeDutyCycle(speed)
    
    def set_motor_b(self, speed, direction):
        GPIO.output(self.in1_b, direction == "forward")
        GPIO.output(self.in2_b, direction == "backward")
        self.pwm_b.ChangeDutyCycle(speed)
        
    def cleanup(self):
        self.pwm_a.stop()
        self.pwm_b.stop()
        GPIO.cleanup()

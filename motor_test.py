import RPi.GPIO as GPIO
import time
import atexit

pwm_pins = [33,15]
on_off_pins1 = [31,29]
on_off_pins2 = [13,11]
INIT_DUTY_CYCLE = 100

def clean_up():
    print("cleaning up :)")
    GPIO.clean_up

# ccw
def toggle_direction_left():
    # left wheel spin backwards
    GPIO.output(31, 1) 
    GPIO.output(29, 0) 
    # right wheel spin forwards
    GPIO.output(13, 0)
    GPIO.output(11, 1)
    
# cw
def toggle_direction_right():
    # left wheel spin forwards
    GPIO.output(31, 0) 
    GPIO.output(29, 1) 
    # right wheel spin backwards
    GPIO.output(13, 1)
    GPIO.output(11, 0)
    
def stop_motors():
    pwm1.stop()
    pwm2.stop()
    
def start_motors():
    pwm1.start(INIT_DUTY_CYCLE)
    pwm2.start(INIT_DUTY_CYCLE)

def go_forward():
    # both wheels spin forward
    GPIO.output(13, 0)
    GPIO.output(11, 1) 
    GPIO.output(31, 0)
    GPIO.output(29, 1)

atexit.register(clean_up)

GPIO.setmode(GPIO.BOARD)
GPIO.setup(pwm_pins, GPIO.OUT)
GPIO.setup(on_off_pins1, GPIO.OUT)
GPIO.setup(on_off_pins2, GPIO.OUT)

pwm1 = GPIO.PWM(33, 50)
pwm1.start(INIT_DUTY_CYCLE)
pwm2 = GPIO.PWM(15, 50)
pwm2.start(INIT_DUTY_CYCLE)

go_forward()
time.sleep(3)

toggle_direction_left():
time.sleep(1)

toggle_direction_right():
time.sleep(2)

go_forward()
time.sleep(2)

GPIO.cleanup()


import RPi.GPIO as GPIO
import time

pwm_pins = [33,15]
on_off_pins = [31,29]
INIT_DUTY_CYCLE = 100

def switch_direction():
    GPIO.output(31, not GPIO.input(31)) # flip flop output pins
    GPIO.output(29, not GPIO.input(29)) # flip flop output pins

def slow_down_for(t_ms):
    init_time = time.time()
    dt = (time.time() - init_time) * 1000 # ms
    while t_ms - dt > 0:
        duty_cycle = t_ms *  
        pwm1.ChangeDutyCycle(duty_cycle)

GPIO.setmode(GPIO.BOARD)
GPIO.setup(pwm_pins, GPIO.OUT)
GPIO.setup(on_off_pins, GPIO.OUT)
pwm1 = GPIO.PWM(33, 50)
pwm1.start(INIT_DUTY_CYCLE)
GPIO.output(31, 1)
GPIO.output(29, 0)
time.sleep(3) # wait for n seconds
switch_direction()
time.sleep(3) # wait for n seconds
#switch_direction()
#time.sleep(1) # wait for n seconds
#switch_direction()
#time.sleep(1) # wait for n seconds
#switch_direction()
GPIO.cleanup()


import RPi.GPIO as GPIO
from time import sleep
import time
import sys

EMULATE_HX711=False

if not EMULATE_HX711:
    import RPi.GPIO as GPIO
    from hx711 import HX711
else:
    from emulated_hx711 import HX711

def cleanAndExit():
    print ("Cleaning...")
    pwm.stop()
    if not EMULATE_HX711:
        GPIO.cleanup()
        
    print ("Bye!")
    sys.exit()

hx = HX711(5, 6)

hx.set_reading_format("MSB", "MSB")

hx.set_reference_unit(92)

hx.reset()

hx.tare()

print ("Tare done! Add weight now...")
hx.tare_A()
hx.tare_B()


#GPIO.setmode(GPIO.BOARD)
GPIO.setup(2,GPIO.OUT)
pwm=GPIO.PWM(2,50)
pwm.start(0)


def setAngle(angle):
    duty=(angle/18)+2 
    GPIO.output(2,True)
    pwm.ChangeDutyCycle(duty)
    sleep(1)
    GPIO.output(2,False)
    pwm.ChangeDutyCycle(0)

setAngle(25)
time.sleep(2)

while True:
    try:
        val = hx.get_weight(5) * -1
        print ("val: %s") % val
        hx.power_down()
        hx.power_up()
        time.sleep(0.1)
        if val <= 100:
          print ("acilacak")
          setAngle(90) #acik
          sleep(2)
        elif val > 100 :
          setAngle(25)
          print ("kapanacak")
          sleep(2)
        time.sleep(5) 
    except (KeyboardInterrupt, SystemExit):
        cleanAndExit()






from ola.ClientWrapper import ClientWrapper
from rpi_ws281x import *
import RPi.GPIO as GPIO
import math

DMX_UNIVERSE = 1

# LED strip configuration:
LED_COUNT      = 270     # Number of LED pixels.
LED_START_ADDR = 1       # DMX Start address
LED_DOUBLING   = 2	 # LEDs per DMX Channel
LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
#LED_PIN        = 10     # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53

# Blinder configuration:
BLIND_START_ADDR =  140   # DMX Start Address of Blinder (has to be > LED_START+LED_COUNT)
BLIND_PWM_FREQ = 10      # PWM Frequency in Hertz for the blinders

def NewData(data):
  # Strips
  for i in range(0,strip.numPixels(),LED_DOUBLING):
     baddr = i/LED_DOUBLING+1+(i/LED_DOUBLING*2)-1
     color = Color(data[baddr],data[baddr+1],data[baddr+2])
     strip.setPixelColor(i, color);
     if(LED_DOUBLING > 1):
       strip.setPixelColor(i+1, color) 
  strip.show()

  # Blinders
  b1Pwm.ChangeDutyCycle(data[BLIND_START_ADDR]/255*100)
  b2Pwm.ChangeDutyCycle(data[BLIND_START_ADDR+1]/255*100)

# Init Strips
strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
strip.begin()  

# Init Blinders
GPIO.setmode(GPIO.BCM)
GPIO.setup(2, GPIO.OUT)
GPIO.setup(3, GPIO.OUT)
b1Pwm = GPIO.PWM(2, BLIND_PWM_FREQ)
b2Pwm = GPIO.PWM(3, BLIND_PWM_FREQ)
b1Pwm.start(0)
b2Pwm.start(0)


# Start listen to OLA
wrapper = ClientWrapper()
client = wrapper.Client()
client.RegisterUniverse(DMX_UNIVERSE, client.REGISTER, NewData)
wrapper.Run()

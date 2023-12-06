import time
from rpi_ws281x import PixelStrip, Color

# LED strip configuration:
LED_COUNT = 21          # Number of LED pixels
LED_PIN = 12            # GPIO pin connected to the pixels (18 uses PWM)
LED_FREQ_HZ = 800000    # LED signal frequency in hertz (usually 800kHz)
LED_DMA = 10            # DMA channel to use for generating signal
LED_BRIGHTNESS = 255    # Set to 0 for darkest and 255 for brightest
LED_INVERT = False      # True to invert the signal (when using NPN transistor level shift)

# Create NeoPixel object
strip = PixelStrip(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS)
strip.begin()

def update_strip():
    # First 10 LEDs one color (e.g., Red)
    for i in range(10):
        strip.setPixelColor(i, Color(255, 0, 0))  # Red

    # Middle LED another color (e.g., White)
    strip.setPixelColor(10, Color(255, 255, 255))  # White

    # Last 10 LEDs another color (e.g., Green)
    for i in range(11, 21):
        strip.setPixelColor(i, Color(0, 255, 0))  # Green

    strip.show()

try:
    while True:
        print("XXXXXXXXXXXX")
        update_strip()
        time.sleep(1)

except KeyboardInterrupt:
    # Turn off all LEDs when Ctrl+C is pressed
    for i in range(LED_COUNT):
        strip.setPixelColor(i, Color(0, 0, 0))
    strip.show()

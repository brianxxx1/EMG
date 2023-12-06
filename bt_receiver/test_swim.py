import board
import neopixel

# Configure the setup
LED_COUNT = 21          # Number of LED pixels.
LED_PIN = board.D12     # GPIO pin connected to the NeoPixels (must support PWM).
ORDER = neopixel.GRB    # Pixel color channel order

# Create the NeoPixel object
strip = neopixel.NeoPixel(LED_PIN, LED_COUNT, brightness=0.5, auto_write=False, pixel_order=ORDER)

def update_strip():
    # First 10 LEDs in red
    for i in range(10):
        strip[i] = (255, 0, 0)  # Red color

    # Middle LED in white
    strip[10] = (255, 255, 255)  # White color

    # Last 10 LEDs in green
    for i in range(11, 21):
        strip[i] = (0, 255, 0)  # Green color

    strip.show()

try:
    while True:
        update_strip()

except KeyboardInterrupt:
    # Turn off all the LEDs on Ctrl+C
    strip.fill((0, 0, 0))
    strip.show()

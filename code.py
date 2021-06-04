import time
from adafruit_funhouse import FunHouse
import board
import neopixel
from digitalio import DigitalInOut, Direction, Pull

#define colors
BLUE = 0x0000FF
RED = 0xFF0000
BLACK = 0x000000
DKGREEN = 0x003300
GREEN = 0x00FF00
DKBLUE = 0x000055
PINK = 0XFE019A

#initialize display items
funhouse = FunHouse(default_bg=None, scale=2)
status_label = funhouse.add_text(text=" ", text_position=(1, 10), text_color=BLUE)
temp_label = funhouse.add_text(text=" ", text_position=(1, 25), text_color=BLUE)
hum_label = funhouse.add_text(text=" ", text_position=(1, 40), text_color=BLUE)
alarm_label = funhouse.add_text(text=" ", text_position=(1, 55), text_color=RED)
light_label = funhouse.add_text(text=" ", text_position=(1, 70), text_color=BLUE)
house_label = funhouse.add_text(text="Barbie's Automated" , text_position=(7, 98), text_color=PINK)
house_label = funhouse.add_text(text="Dreamhouse" , text_position=(30, 113), text_color=PINK)
funhouse.display.show(funhouse.splash)
#initialize neopixel strip
pixel = neopixel.NeoPixel(board.A0, 30, pixel_order=neopixel.RGB)
#initialize breakbeam sensor
sensor = DigitalInOut(board.A1)
sensor.direction = Direction.INPUT
sensor.pull = Pull.UP
#initliaze variables
alarm = False
brightness = 0

#main loop
while True:
    #read these sensors during normal operations
    funhouse.set_text("Temp %0.0F F" % (funhouse.peripherals.temperature * 9 / 5 + 22), temp_label)
    funhouse.set_text("Hum %0.1F %%" % funhouse.peripherals.relative_humidity, hum_label)
    #the next line shows True when breakbeam sensor is working properly to assist in proper alignment, it can be commentted out or deleted after setting up
    funhouse.set_text(sensor.value, light_label)
    
    #only enter this portion if the alarm is set
    if alarm:
        funhouse.set_text_color(GREEN, status_label)
        funhouse.set_text("Alarm Set", status_label)
        #alarm triggered by break beam sensor
        if not sensor.value:
            while True:
                #flash alternating red dotstars and clear screen while alarm is flashing
                funhouse.peripherals.set_dotstars(BLACK, RED, BLACK, RED, BLACK)
                pixel.fill((0, 0, 0))
                funhouse.set_text(" ", temp_label)
                funhouse.set_text(" ", status_label)
                funhouse.set_text(" ", light_label)
                funhouse.set_text(" ", hum_label)
                funhouse.set_text("      ALARM!", alarm_label)
                time.sleep(.25)
                funhouse.set_text(" ", alarm_label)
                funhouse.peripherals.set_dotstars(RED, BLACK, RED, BLACK, RED)
                pixel.fill((0, 255, 0))
                funhouse.peripherals.play_tone(440, 0.5)
                #press any button to clear alarm, green lights to acknowledge alarm has been disable and 2 sec wait as a debounce
                if funhouse.peripherals.button_sel or funhouse.peripherals.button_up or funhouse.peripherals.button_down:
                    funhouse.peripherals.set_dotstars(DKGREEN, DKGREEN, DKGREEN, DKGREEN, DKGREEN)
                    pixel.fill((51, 0, 0))
                    time.sleep(2)
                    #ensures that the dotstars are off and returns neopixels to original brightness
                    funhouse.peripherals.set_dotstars(BLACK, BLACK, BLACK, BLACK, BLACK)
                    pixel.fill((brightness,brightness,brightness))
                    alarm = False
                    break
    #notifies that the alarm is not set
    elif not alarm:
        funhouse.set_text_color(RED, status_label)
        funhouse.set_text("Alarm Not Set", status_label)

    #uses the slider as a dimmer for the neopixel strip
    slider = funhouse.peripherals.slider
    if slider is not None:
        brightness = int(slider * 255)
        pixel.fill((brightness,brightness,brightness))

    #the up button is used to toggle the alarm between set and not set
    if funhouse.peripherals.button_up:
        if not alarm:
            alarm = True
            funhouse.set_text("ALARM SET", alarm_label)
            time.sleep(1)
            funhouse.set_text(" ", alarm_label)
        elif alarm:
            alarm = False
            funhouse.set_text("ALARM OFF", alarm_label)
            time.sleep(1)
            funhouse.set_text(" ", alarm_label)

    #the capactive touch buttons are used to induce three different weather warnings with flashing blue dotstars and neopixels
    #any real button (up, sel, down) will clear the weather warning
    if funhouse.peripherals.captouch6:
        alarm = False
        while True:
            funhouse.set_text("EARTHQUAKE WARNING!", alarm_label)
            funhouse.peripherals.set_dotstars(BLACK, BLACK, BLACK, BLACK, BLACK)
            pixel.fill((0, 0, 0))
            time.sleep(.5)
            funhouse.peripherals.set_dotstars(DKBLUE, DKBLUE, DKBLUE, DKBLUE, DKBLUE)
            pixel.fill((0, 0, 85))
            funhouse.set_text(" ", alarm_label)
            time.sleep(.5)
            if funhouse.peripherals.button_sel or funhouse.peripherals.button_up or funhouse.peripherals.button_down:
                funhouse.peripherals.set_dotstars(DKGREEN, DKGREEN, DKGREEN, DKGREEN, DKGREEN)
                pixel.fill((51, 0, 0))
                time.sleep(1)
                funhouse.peripherals.set_dotstars(BLACK, BLACK, BLACK, BLACK, BLACK)
                pixel.fill((brightness,brightness,brightness))

                break
    
    if funhouse.peripherals.captouch7:
        alarm = False
        while True:
            funhouse.set_text(" HURRICANE WARNING!", alarm_label)
            funhouse.peripherals.set_dotstars(BLACK, BLACK, BLACK, BLACK, BLACK)
            pixel.fill((0, 0, 0))
            time.sleep(.5)
            funhouse.peripherals.set_dotstars(DKBLUE, DKBLUE, DKBLUE, DKBLUE, DKBLUE)
            pixel.fill((0, 0, 85))
            funhouse.set_text(" ", alarm_label)
            time.sleep(.5)
            if funhouse.peripherals.button_sel or funhouse.peripherals.button_up or funhouse.peripherals.button_down:
                funhouse.peripherals.set_dotstars(DKGREEN, DKGREEN, DKGREEN, DKGREEN, DKGREEN)
                pixel.fill((51, 0, 0))
                time.sleep(1)
                funhouse.peripherals.set_dotstars(BLACK, BLACK, BLACK, BLACK, BLACK)
                pixel.fill((brightness,brightness,brightness))
                break
            
    if funhouse.peripherals.captouch8:
        alarm = False
        while True:
            funhouse.set_text("  TORNADO WARNING!", alarm_label)
            funhouse.peripherals.set_dotstars(BLACK, BLACK, BLACK, BLACK, BLACK)
            pixel.fill((0, 0, 0))
            time.sleep(.5)
            funhouse.peripherals.set_dotstars(DKBLUE, DKBLUE, DKBLUE, DKBLUE, DKBLUE)
            pixel.fill((0, 0, 85))
            funhouse.set_text(" ", alarm_label)
            time.sleep(.5)
            if funhouse.peripherals.button_sel or funhouse.peripherals.button_up or funhouse.peripherals.button_down:
                funhouse.peripherals.set_dotstars(DKGREEN, DKGREEN, DKGREEN, DKGREEN, DKGREEN)
                pixel.fill((51, 0, 0))
                time.sleep(1)
                funhouse.peripherals.set_dotstars(BLACK, BLACK, BLACK, BLACK, BLACK)
                pixel.fill((brightness,brightness,brightness))
                break

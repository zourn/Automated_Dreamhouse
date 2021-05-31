import time
from adafruit_funhouse import FunHouse
import board
import neopixel
from digitalio import DigitalInOut, Direction, Pull

#initialize display items
funhouse = FunHouse(default_bg=None, scale=2)
status_label = funhouse.add_text(text=" " , text_position=(1, 10), text_color=0x0000FF)
temp_label = funhouse.add_text(text=" " , text_position=(1, 25), text_color=0x0000FF)
hum_label = funhouse.add_text(text=" " , text_position=(1, 40), text_color=0x0000FF)
alarm_label = funhouse.add_text(text=" " , text_position=(1, 55), text_color=0xFF0000)
light_label = funhouse.add_text(text=" " , text_position=(1, 70), text_color=0x0000FF)
house_label = funhouse.add_text(text="Barbie's Automated" , text_position=(7, 98), text_color=0xFE019A)
house_label = funhouse.add_text(text="Dreamhouse" , text_position=(30, 113), text_color=0xFE019A)
funhouse.display.show(funhouse.splash)
#initialize neopixel strip
pixel = neopixel.NeoPixel(board.A0, 30, pixel_order=neopixel.RGB)
#initialize breakbeam sensor
sensor = DigitalInOut(board.A1)
sensor.direction = Direction.INPUT
sensor.pull = Pull.UP
#initliaze variables
alarm = 0
brightness = 0

#main loop
while True:
    #read these sensors during normal operations
    funhouse.set_text("Temp %0.0F F" % (funhouse.peripherals.temperature * 9 / 5 + 22), temp_label)
    funhouse.set_text("Hum %0.1F %%" % funhouse.peripherals.relative_humidity, hum_label)
    #the next line shows True when breakbeam sensor is working properly to assist in proper alignment, it can be commentted out or deleted after setting up
    funhouse.set_text(sensor.value, light_label)
    
    #only enter this portion if the alarm is set
    if alarm == 1:
        funhouse.set_text_color(0x00FF00, status_label)
        funhouse.set_text("Alarm Set", status_label)
        #alarm triggered by break beam sensor
        if not sensor.value:
            while True:
                #flash alternating red dotstars and clear screen while alarm is flashing
                funhouse.peripherals.set_dotstars(0x000000, 0xFF0000, 0x000000, 0xFF0000, 0x000000)
                pixel.fill((0, 0, 0))
                funhouse.set_text(" ", temp_label)
                funhouse.set_text(" ", status_label)
                funhouse.set_text(" ", light_label)
                funhouse.set_text(" ", hum_label)
                funhouse.set_text("      ALARM!", alarm_label)
                time.sleep(.25)
                funhouse.set_text(" ", alarm_label)
                funhouse.peripherals.set_dotstars(0xFF0000, 0x000000, 0xFF0000, 0x000000, 0xFF0000)
                pixel.fill((0, 255, 0))
                funhouse.peripherals.play_tone(440, 0.5)
                #press any button to clear alarm, green lights to acknowledge alarm has been disable and 2 sec wait as a debounce
                if funhouse.peripherals.button_sel or funhouse.peripherals.button_up or funhouse.peripherals.button_down:
                    funhouse.peripherals.set_dotstars(0x003300, 0x003300, 0x00AA00, 0x003300, 0x003300)
                    pixel.fill((51, 0, 0))
                    time.sleep(2)
                    #ensures that the dotstars are off and returns neopixels to original brightness
                    funhouse.peripherals.set_dotstars(0x000000, 0x000000, 0x000000, 0x000000, 0x000000)
                    pixel.fill((brightness,brightness,brightness))
                    alarm = 0
                    break
    #notifies that the alarm is not set
    elif alarm == 0:
        funhouse.set_text_color(0xFF0000, status_label)
        funhouse.set_text("Alarm Not Set", status_label)

    #uses the slider as a dimmer for the neopixel strip
    slider = funhouse.peripherals.slider
    if slider is not None:
        brightness = int(slider * 255)
        pixel.fill((brightness,brightness,brightness))

    #the up button is used to toggle the alarm between set and not set
    if funhouse.peripherals.button_up:
        if alarm == 0:
            alarm = 1
            funhouse.set_text("ALARM SET", alarm_label)
            time.sleep(1)
            funhouse.set_text(" ", alarm_label)
        elif alarm == 1:
            alarm = 0
            funhouse.set_text("ALARM OFF", alarm_label)
            time.sleep(1)
            funhouse.set_text(" ", alarm_label)

    #the capactive touch buttons are used to induce three different weather warnings with flashing blue dotstars and neopixels
    #any real button (up, sel, down) will clear the weather warning
    if funhouse.peripherals.captouch6:
        alarm = 0
        while True:
            funhouse.set_text("EARTHQUAKE WARNING!", alarm_label)
            funhouse.peripherals.set_dotstars(0x000000, 0x000000, 0x000000, 0x000000, 0x000000)
            pixel.fill((0, 0, 0))
            time.sleep(.5)
            funhouse.peripherals.set_dotstars(0x000055, 0x000055, 0x000055, 0x000055, 0x000055)
            pixel.fill((0, 0, 85))
            funhouse.set_text(" ", alarm_label)
            time.sleep(.5)
            if funhouse.peripherals.button_sel or funhouse.peripherals.button_up or funhouse.peripherals.button_down:
                funhouse.peripherals.set_dotstars(0x000000, 0x000000, 0x000000, 0x000000, 0x000000)
                pixel.fill((brightness,brightness,brightness))
                time.sleep(1)
                break
    
    if funhouse.peripherals.captouch7:
        alarm = 0
        while True:
            funhouse.set_text(" HURRICANE WARNING!", alarm_label)
            funhouse.peripherals.set_dotstars(0x000000, 0x000000, 0x000000, 0x000000, 0x000000)
            pixel.fill((0, 0, 0))
            time.sleep(.5)
            funhouse.peripherals.set_dotstars(0x000055, 0x000055, 0x000055, 0x000055, 0x000055)
            pixel.fill((0, 0, 85))
            funhouse.set_text(" ", alarm_label)
            time.sleep(.5)
            if funhouse.peripherals.button_sel or funhouse.peripherals.button_up or funhouse.peripherals.button_down:
                funhouse.peripherals.set_dotstars(0x000000, 0x000000, 0x000000, 0x000000, 0x000000)
                pixel.fill((brightness,brightness,brightness))
                time.sleep(1)
                break
            
    if funhouse.peripherals.captouch8:
        alarm = 0
        while True:
            funhouse.set_text("  TORNADO WARNING!", alarm_label)
            funhouse.peripherals.set_dotstars(0x000000, 0x000000, 0x000000, 0x000000, 0x000000)
            pixel.fill((0, 0, 0))
            time.sleep(.5)
            funhouse.peripherals.set_dotstars(0x000055, 0x000055, 0x000055, 0x000055, 0x000055)
            pixel.fill((0, 0, 85))
            funhouse.set_text(" ", alarm_label)
            time.sleep(.5)
            if funhouse.peripherals.button_sel or funhouse.peripherals.button_up or funhouse.peripherals.button_down:
                funhouse.peripherals.set_dotstars(0x000000, 0x000000, 0x000000, 0x000000, 0x000000)
                pixel.fill((brightness,brightness,brightness))
                time.sleep(1)
                break

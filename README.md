# Automated_Dreamhouse
Barbie's Automated Dreamhouse

This is a CircuitPython project that uses an Adafruit Funhouse as the base unit with:
* A0: 30-unit Neopixel strip
* A1: Break beam reciever
* A2: Break beam transmitter
  
The Neopixel strip acts as a lighting strip and can be controlled using the capacitive slider on the Funhouse as a dimmer switch. It will also flash red with the alarm, and blue with the weather alerts.
The normal screen shows:
	
* Alarm Not Set/Alarm Set
* Temperature (this may need tweaking to adjust for sensor bias)
* Humidity
* Breakbeam status (until the line is commented out or deleted)
* 'Barbie's Automated Dreamhouse'
	
The alarm defaults to 'Not Set' on boot. Use the top button to set the alarm. An on-screen notification will show that the alarm is now set.
While the alarm is set, an object passing through the break-beam sensor will cause the speaker to sound, the Neopixels to flash red, the on-board dotstars to flash red, and the word 'ALARM! to flash on the screen.
Pressing any of the real buttons along the side of the screen will stop the alarm and change the alarm to 'Not Set'.
The capacitive buttons will start a weather alert which flashes the type of weather alert on the screen, and flash the Neopixel strip and the on-board dotstars blue:
	
* C16: Earthquake Warning
* C17: Hurricane Warning
* C18: Tornado Warning
	
Pressing any of the real buttons along the side of the screen will stop the weather alert.

When pressing a button to stop the alarm or the weather alert, hold the button until the LEDs show green.

The secrets.py file is needed to be read by the Funhouse standard library, but the data is never used in this project so there is no need to change the information in secrets.py.

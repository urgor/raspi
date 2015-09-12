#!/usr/bin/python3

import lirc, math
import time, RPi.GPIO as GPIO
from subprocess import call
from lcd_16x2 import *

# GPIO.setmode(GPIO.BOARD)
GPIO.setmode(GPIO.BCM)
valve1 = 19
valve2 = 26
shutterDelay = 0.05
shutterStep = 0.01
GPIO.setup(valve1, GPIO.OUT)
GPIO.setup(valve2, GPIO.OUT)
sockid = lirc.init("myprogram")
lcd_init();

def displayMenu(i):
	lcd_string(menu[i]['menu'], LCD_LINE_1)
	lcd_string(str(menu[i]['value'])+' ['+str(menu[i]['step'])+']', LCD_LINE_2)

def drop(valve):
	GPIO.output(valve, 1)
	time.sleep(0.05)
	GPIO.output(valve, 0)

menu = [
	{'menu' : 'Valve 1 delay ..', 'value' : 0.02, 'step' : 0.01},
	{'menu' : 'Valve 2 delay ..', 'value' : 'off', 'step' : 0.01},
	{'menu' : 'Sutter delay  .|', 'value' : 0.05, 'step' : 0.01}
]
activeItem = 0
displayMenu(activeItem)
print("Ready")
try:
	while True:
		code = lirc.nextcode()

		if 0 == len(code):
			print('unknow key code')
			continue

		if 'KEY_OK' == code[0]:
			if not menu[0]['value'] == 'off':
				drop(valve1)
				if menu[0]['value'] > 0:
					time.sleep(menu[0]['value'])
					drop(valve1)
			if not menu[1]['value'] == 'off':
				drop(valve2)
				if menu[1]['value'] > 0:
					time.sleep(menu[1]['value'])
					drop(valve2)
			if not menu[2]['value'] == 'off':
				if menu[2]['value'] > 0:
					time.sleep(menu[2]['value'])
				call(['irsend', 'SEND_ONCE', 'nikon', 'shutter'])
		
		elif 'KEY_LEFT' == code[0]:
			if activeItem == 0: continue
			activeItem -= 1
			displayMenu(activeItem)

		elif 'KEY_RIGHT' == code[0]:
			if activeItem == 2: continue
			activeItem += 1
			displayMenu(activeItem)
		
		elif 'KEY_UP' == code[0]: # increment
			if menu[activeItem]['value'] == 'off': menu[activeItem]['value'] = 0
			menu[activeItem]['value'] += menu[activeItem]['step']
			digits = round(math.log10(1/menu[activeItem]['step']))
			menu[activeItem]['value'] = round(menu[activeItem]['value'], digits)
			if menu[activeItem]['value'] == menu[activeItem]['step'] * 10 :
				menu[activeItem]['step'] = menu[activeItem]['step'] * 10
			displayMenu(activeItem)

		elif 'KEY_DOWN' == code[0]: # decrement
			if menu[activeItem]['value'] == 'off': continue
			if menu[activeItem]['value'] == menu[activeItem]['step']:
				menu[activeItem]['step'] = menu[activeItem]['step'] / 10
			menu[activeItem]['value'] -= menu[activeItem]['step']
			digits = round(math.log10(1/menu[activeItem]['step']))
			menu[activeItem]['value'] = round(menu[activeItem]['value'], digits)
			displayMenu(activeItem)

		elif 'KEY_0' == code[0]:
			menu[activeItem]['value'] = 0
			displayMenu(activeItem)

		elif 'KEY_A' == code[0]:
			menu[activeItem]['value'] = 'off'
			displayMenu(activeItem)

		elif 'KEY_B' == code[0]:
			call(['shutdown', 'now'])
			raise Exception('Goodbye')


except KeyboardInterrupt:
	pass
# except Exception as e:
# 	print(type(e))
# 	print(e.args)
# 	print(e)
finally:
	lcd_byte(0x01, LCD_CMD)
	lcd_string("Goodbye!",LCD_LINE_1)
	GPIO.cleanup()

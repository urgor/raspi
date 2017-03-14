import RPi.GPIO as GPIO
import I2C_LCD_driver
import time

mylcd = I2C_LCD_driver.lcd()


# mylcd.lcd_display_string("This is how you", 1)
# sleep(1)
# mylcd.lcd_clear()
# mylcd.lcd_display_string("clear the screen", 1)
# sleep(1)
# mylcd.lcd_clear()

# while True:
#     mylcd.lcd_display_string("Time: %s" %time.strftime("%H:%M:%S"), 1)
#     mylcd.lcd_display_string("Date: %s" %time.strftime("%m/%d/%Y"), 2)
#     time.sleep(1)

# str_pad = " " * 16
# my_long_string = "This is a string that needs to scroll"
# my_long_string = str_pad + my_long_string
# while True:
#     for i in range (0, len(my_long_string)):
#         lcd_text = my_long_string[i:(i+16)]
#         mylcd.lcd_display_string(lcd_text,1)
#         time.sleep(0.4)
#         mylcd.lcd_display_string(str_pad,1)
#


mylcd.lcd_display_string('Urgor', 1)
mylcd.lcd_display_string('urgor@gmail.com', 2)
mylcd.backlight(1)

# fontdata1 = [
#         # char(0) - Upper-left character
#         [ 0b00000,
#           0b00000,
#           0b00000,
#           0b00000,
#           0b00000,
#           0b00000,
#           0b11111,
#           0b11111 ],
#         # char(1) - Upper-middle character
#         [ 0b00000,
#           0b00000,
#           0b00100,
#           0b00110,
#           0b00111,
#           0b00111,
#           0b11111,
#           0b11111 ],
#         # char(2) - Upper-right character
#         [ 0b00000,
#           0b00000,
#           0b00000,
#           0b00000,
#           0b00000,
#           0b00000,
#           0b10000,
#           0b11000 ],
#         # char(3) - Lower-left character
#         [ 0b11111,
#           0b11111,
#           0b00000,
#           0b00000,
#           0b00000,
#           0b00000,
#           0b00000,
#           0b00000 ],
#         # char(4) - Lower-middle character
#         [ 0b11111,
#           0b11111,
#           0b00111,
#           0b00111,
#           0b00110,
#           0b00100,
#           0b00000,
#           0b00000 ],
#         # char(5) - Lower-right character
#         [ 0b11000,
#           0b10000,
#           0b00000,
#           0b00000,
#           0b00000,
#           0b00000,
#           0b00000,
#           0b00000 ],
# ]
# mylcd.lcd_load_custom_chars(fontdata1)
# mylcd.lcd_write(0x80)
# mylcd.lcd_write_char(0)
# mylcd.lcd_write_char(1)
# mylcd.lcd_write_char(2)
# mylcd.lcd_write(0xC0)
# mylcd.lcd_write_char(3)
# mylcd.lcd_write_char(4)
# mylcd.lcd_write_char(5)




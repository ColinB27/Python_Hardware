"""
    LCD_Lib.py
Personal library for use with a 20x4 LCD screen (2004A)
This library allows the creation of objects capable of managing LCD screens: writing, clearing, etc.

This version is highly inspired by examples found on the internet but is optimized as an object. 
I have kept only the necessary elements.

--Author     : Colin Boulé
--Revision   : 002
--First Rev. : 2023/01/30
--Last Rev.  : 2024/02/27
"""
#-------------------------------------- Dependencies  --------------------------------------#
import machine
from machine import Pin
import time
import utime

#---------------------------------------- References ---------------------------------------#
LCD_LINE_1 = 0x80 # LCD RAM address for the 1st line
LCD_LINE_2 = 0xC0 # LCD RAM address for the 2nd line
LCD_LINE_3 = 0x94 # LCD RAM address for the 3rd line
LCD_LINE_4 = 0xD4 # LCD RAM address for the 4th line
LCD_CLR = 0x01            
LCD_HOME = 0x02
LCD_MOVE_RIGHT = 0x04
LCD_ON_BLINK = 0x01
LCD_ON_CURSOR = 0x02
#--------------------------------------------------------------------------------------------#

class Lcd2004:
    def __init__(self, rs, en, d4, d5, d6, d7):
        self.rs = machine.Pin(rs,machine.Pin.OUT)
        self.en  = machine.Pin(en,machine.Pin.OUT)
        self.d4 = machine.Pin(d4,machine.Pin.OUT)
        self.d5 = machine.Pin(d5,machine.Pin.OUT)
        self.d6 = machine.Pin(d6,machine.Pin.OUT)
        self.d7 = machine.Pin(d7,machine.Pin.OUT)
        
    def pulseEN(self):
        (self.en).value( 1)
        utime.sleep_us(40)
        (self.en).value( 0)
        utime.sleep_us(40)
        
    def send2LCD4(self,char):
        (self.d4).value((char & 0b00000001) >>0)
        (self.d5).value((char & 0b00000010) >>1)
        (self.d6).value((char & 0b00000100) >>2)
        (self.d7).value((char & 0b00001000) >>3)
        self.pulseEN()
        
    def send2LCD8(self,char):
        (self.d4).value((char & 0b00010000) >>4)
        (self.d5).value((char & 0b00100000) >>5)
        (self.d6).value((char & 0b01000000) >>6)
        (self.d7).value((char & 0b10000000) >>7)
        self.pulseEN()
        (self.d4).value((char & 0b00000001) >>0)
        (self.d5).value((char & 0b00000010) >>1)
        (self.d6).value((char & 0b00000100) >>2)
        (self.d7).value((char & 0b00001000) >>3)
        self.pulseEN()
        
    def setUpLCD(self):
        (self.rs).value(0)
        self.send2LCD4(0b0011) #8 bit
        self.send2LCD4(0b0011) #8 bit
        self.send2LCD4(0b0011) #8 bit
        self.send2LCD4(0b0010) #4 bit
        self.send2LCD8(0b00101000) #4 bit,2 lines?,5*8 bots
        self.send2LCD8(0b00001100) #lcd on, blink off, cursor off. (0b 00 00 00 00 ) => (00 00 00 blink)
        self.send2LCD8(0b00000110) #increment cursor, no display shift
        self.send2LCD8(0b00000001) #clear screen
        utime.sleep_ms(2) #clear screen needs a long delay
        
    def writeStr(self,string):
        (self.rs).value(1)
        for x in string:
            self.send2LCD8(ord(x))
            
    def writeCmd(self,char):
        (self.rs).value(0)
        self.send2LCD4(0b0011) #8 bit
        self.send2LCD4(0b0011) #8 bit
        self.send2LCD4(0b0011) #8 bit
        self.send2LCD4(0b0010) #4 bit
        self.send2LCD8(char) #clear screen
        
  def writeStrToLine(self,string,line):
        lines = [LCD_LINE_1,LCD_LINE_2,LCD_LINE_3,LCD_LINE_4]
        if line >= 1 and line <= 4:
          self.writeCmd(lines[line])
          self.writeStr(string)
  def clear(self):
        self.writeCmd(LCD_CLR)

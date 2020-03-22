# -*- coding: utf-8 -*- using python3
# Example: Scrape and Parse COVID-19 data from sanantonio.gov to be displayed on console and 16x2 LCD
# I'm still learning python, I know this can be done way easier!
# Make sure to follow Maker Tutor's video on using the 16x2 LCD with RPi https://www.youtube.com/watch?v=3XLjVChVgec
# you will need to put this program in the lcd folder and rename the folder CoVID_data or something
# dont forget to check out the BeautifulSoup documentation as well! https://beautiful-soup-4.readthedocs.io/en/latest/
# https://www.dataquest.io/blog/web-scraping-tutorial-python/
# I have also made a desktop shortcut that calls a bash script that calls this program in a console



#Coded by the gilded pantaloon aka the phonesgetti with lots of research and thonny IDE

import os
import requests
from bs4 import BeautifulSoup
import time
import lcddriver
import re

display = lcddriver.lcd()


# scroll text on 1st row lcd

def long_string(display, text = '', num_line = 1, num_cols = 16):
    if(len(text) > num_cols):
        display.lcd_display_string(text[:num_cols],num_line)
        time.sleep(2)
        for i in range(len(text) - num_cols + 1):
            text_to_print = text[i:i+num_cols]
            display.lcd_display_string(text_to_print,num_line)
            time.sleep(0.4)
        time.sleep(1)
    else:
        display.lcd_display_string(text,num_line)


# subract 2 strings

def subtract_str(a,b):
    return "".join(a.rsplit(b))


# convert a list to string

def listToString(s):
    # initialize an empty string
    str1 = ""
    # traverse in the string
    for ele in s:
        str1 += ele
    # return string
    return str1


#extract numbers from string as list and convert to string
def getNumbers(str):
        array = re.findall(r'[0-9]+', str)
        return listToString(array)

#program start

print("----Fetching Data----")

URL = 'https://www.sanantonio.gov/Health/News/Alerts/CoronaVirus'

page = requests.get(URL) #webpage stored

soup = BeautifulSoup(page.content, 'html.parser')

dataTable = soup.find_all('tbody')[0] #you will have to inspect your specific webpage
				      #and change this accordingly
				      #sanantonio.gov displays a couple tables with data
				      #the first table is the one I want so no need to specify a table
				      #when I can jump straight to the tbody

os.system('clear') #clear console

print("\n\n","---------------------")

SAcovidData = list(dataTable) #convert data into list
			      #again, this next part is specific to this particular webpage
			      #by breaking apart my table data I can choose an index-
			      #that represents a table row

#This piece of data (total) will look like
# Total Confirmed cases Bexar County(a number)

total = str(SAcovidData[1].get_text("", strip=True))
travel_related = str(SAcovidData[3].get_text("", strip=True))
close_contact = str(SAcovidData[5].get_text("", strip=True))
community_transmission = str(SAcovidData[7].get_text("", strip=True))
under_investigation = str(SAcovidData[9].get_text("", strip=True))
deaths = str(SAcovidData[11].get_text("", strip=True))


#this next piece of code will copy numbers in the string
#Why? because I want to store the numbers in a different variable to
#be displayed on the second row of my 16x2 I2C lcd

total_number = getNumbers(total)
travel_related_number = getNumbers(travel_related)
close_contact_number = getNumbers(close_contact)
community_transmission_number = getNumbers(community_transmission)
under_investigation_number = getNumbers(under_investigation)
deaths_number = getNumbers(deaths)


#subtract the copied number(which is a string at this point)
#from the original piece of data

total = subtract_str(total, total_number)
travel_related = subtract_str(travel_related, travel_related_number)
close_contact = subtract_str(close_contact, close_contact_number)
community_transmission = subtract_str(community_transmission, community_transmission_number)
under_investigation = subtract_str(under_investigation, under_investigation_number)
deaths = subtract_str(deaths, deaths_number)


#print data on console
#will look like
#-------------------
#Total Confirmed cases Bexar County
#(total_number) 

print(total)
print(total_number, "\n")

print(travel_related)
print(travel_related_number, "\n")

print(close_contact)
print(close_contact_number, "\n")

print(community_transmission)
print(community_transmission_number, "\n")

print(under_investigation)
print(under_investigation_number, "\n")

print(deaths)
print(deaths_number)

# Main body of code , print to lcd

try:
    while True:
        # Remember that your sentences can only be 16 characters long!
        
        display.lcd_display_string(total_number, 2) #Write line of text to second line of display
        long_string(display, total, 1) # Write line of text to first line of display
          
        time.sleep(2)                                    # Give time for the message to be read
        display.lcd_clear()
        
        display.lcd_display_string(travel_related_number, 2) #Write line of text to second line of display 
        long_string(display, travel_related, 1) # Write line of text to first line of display
        
        time.sleep(2)                                     # Give time for the message to be read
        display.lcd_clear()
        
        display.lcd_display_string(close_contact_number, 2) # Refresh the first line of display with a different message
        long_string(display, close_contact, 1) # Write line of text to first line of display
        
        time.sleep(2)
        display.lcd_clear()
        
        display.lcd_display_string(community_transmission_number, 2) # Refresh the first line of display with a different message
        long_string(display, community_transmission, 1) # Write line of text to first line of display
        
        time.sleep(2)
        display.lcd_clear()
        
        display.lcd_display_string(under_investigation_number, 2) # Refresh the first line of display with a different message
        long_string(display, under_investigation, 1) # Write line of text to first line of display
        
        time.sleep(2)
        display.lcd_clear()
        
        display.lcd_display_string(deaths_number, 2) # Refresh the first line of display with a different message
        long_string(display, deaths, 1) # Write line of text to first line of display
        
        time.sleep(2)
        display.lcd_clear()                               # Clear the display of any data
        time.sleep(2)                                     # Give time for the message to be read

except KeyboardInterrupt: # If there is a KeyboardInterrupt (when you press ctrl+c), exit the program and cleanup
    print("Cleaning up!")
    display.lcd_clear()


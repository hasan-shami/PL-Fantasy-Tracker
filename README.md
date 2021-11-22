# PL-Fantasy-Tracker
Tracking changes to player stats on Fantasy Premier League

## Description

This script, in its current format, automatically extracts player information from the English Premier League's fantasy football website and updates a local Excel file with the data available. 

## Installation/Dependencies

 - Anaconda distribution of Python 3.7
 - Selenium library on Python and the Selenium Webdriver extension for Chrome (make sure your Webdriver is the suitable executable depending on your Chrome version)
 - Pandas library for Python
 - Fantasy Premier League website

## Current Implementation/Future Steps

The current implementation, when the script is executed, extracts the current available data of all players in the Premier League. It is important that the script is launched routinely to keep track of any changes by the day. 

The script extracts the following:
 - Name
 - Team
 - Position
 - Cost
 - Form
 - % Selected by
 - Playing chance (in case of injury)
 - Total points

There is loads of room for improvement, with different degrees of complexity, in several areas:

 - Calculate points per gameweek
 - Updating the master file on Google Sheets rather than using a local file, to enable updating the file from different devices
 - Extract further datapoints (goals, assists, clean sheets, etc..)
 - Add a data visualization element where players can be visually filtered and plots can be automatically generated

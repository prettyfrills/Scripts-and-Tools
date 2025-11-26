'''
The purpose of this script is to parse CSVs exported from Mod Organizer 2 and convert the listed mods
into HTML code that hyperlinks to the Nexus Mods page. I made this because I was listing a large number
of Skyrim mods on my website and noticed the task became highly repetitive, making it a good candidate for automation.
'''
import os
import csv

csvPath = "mods.csv"
fields = []
rows = []
outFile = open('outcode.txt', 'w')
link = "https://www.nexusmods.com/skyrimspecialedition/mods/"

with open(csvPath, 'r') as file:
    reader = csv.reader(file)
    fields = next(reader)
    for row in reader:
        if row[1] != '-1':
            rows.append(row)

    for row in rows:
        modName = row[0]
        nexusLink = link + row[1]
        htmlCode = f'<li><a href="{nexusLink}" target="_blank" rel="noopener noreferrer"> {modName} </a></li>'
        outFile.write(htmlCode + '\n')
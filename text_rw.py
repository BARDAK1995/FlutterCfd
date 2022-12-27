# -*- coding: utf-8 -*-
"""
Created on Thu Dec 15 10:31:30 2022

@author: gunes
"""
import csv
def text_write2(text_name,to_be_searched,new_line,wfile_name):
    # Open the file in read mode
    with open(text_name, "r") as f:
    # Read the file into a string
        text = f.read()
    splited_text_0 = text.split(to_be_searched)
    splited_text_1 = splited_text_0[1].split(")")
    lines_until_line_to_changed=text.split(to_be_searched)[0]
    index=lines_until_line_to_changed.count("\n")
    to_be_removed=splited_text_1[0].count("\n")
    lines = text.split("\n")
    lines=lines[:index]+lines[index+to_be_removed:]
    lines[index] = new_line
    # Join the lines back into a single string
    text = "\n".join(lines)
    # Open the file in write mode
    with open(wfile_name, "w") as f:
    # Write the updated text to the file
        f.write(text)
    return()
def text_write(text_name,to_be_searched,new_line,wfile_name):
    # Open the file in read mode
    with open(text_name, "r") as f:
    # Read the file into a string
        text = f.read()
    lines_until_line_to_changed=text.split(to_be_searched)[0]
    index=lines_until_line_to_changed.count("\n")
    lines = text.split("\n")
    lines[index] = new_line
    # Join the lines back into a single string
    text = "\n".join(lines)
    # Open the file in write mode
    with open(wfile_name, "w") as f:
    # Write the updated text to the file
        f.write(text)
    return()
def readcsv(filename):
    # Open the CSV file
    with open(filename, 'r') as file:
      # Create a CSV reader object
      rows= list(csv.reader(file))
      Mamp=float(rows[-1][0])
      Mphase=float(rows[-1][1])
      Lamp=float(rows[-1][2])
      Lphase=float(rows[-1][3])
      
    return(Lamp,Lphase,Mamp,Mphase)
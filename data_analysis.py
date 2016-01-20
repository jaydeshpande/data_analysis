__author__ = 'JD'
import pandas as pd
import numpy as np
import os
from itertools import groupby
rootdir = os.getcwd()
pd.core.format.header_style = None

def main():
    data = pd.read_csv('temperature', delimiter=r"\s+", skiprows=4)
    data2 = pd.read_csv('massflux', delimiter=r"\s+", skiprows=3)
    permeate_temp_inlet=data.iat[0,1]
    saline_temp_inlet=data.iat[2,1]
    permeate_temp_outlet=data.iat[1,1]
    saline_temp_outlet=data.iat[3,1]
    permeate_flow_inlet=data2.iat[0,1]
    permeate_flow_outlet=data2.iat[1,1]
    saline_flow_inlet=data2.iat[2,1]
    saline_flow_outlet=data2.iat[3,1]
    values=[permeate_temp_inlet,saline_temp_inlet,permeate_temp_outlet,saline_temp_outlet,permeate_flow_inlet,saline_flow_inlet,permeate_flow_outlet,saline_flow_outlet]
    return values

for subdir, dirs, files in os.walk(rootdir):
    df = pd.DataFrame(columns=['no', 'id', 'vf', 'tpi', 'tsi', 'tpo', 'tso', 'mdotpi', 'mdotsi', 'mdotpo', 'mdotso', 'arrangement', 'packing angle']) #Create headers for the dataframe
    i = 1 #Incremental counter for row numbering, gives me number of folders in a directory
    basedir = rootdir #Brings the root directory so I don't mess with the variable at the top, in case required at a later point it stays safe
    for dir in dirs:
        name_split2=[''.join(g) for _, g in groupby(dir, str.isalpha)] #Split directory name into groups of numbers and letters
        print name_split2
        newdir = os.path.join(basedir,dir) #Find out directory path for subfolder
        os.chdir(newdir) #Change directory to the new directory
        print os.getcwd() #Debug step -- check if the directory has been changed
        column2 = main() #Returns values of temperature and massflow rates
        column1 = [i,name_split2[0],name_split2[2]] #Stores 3 variables
        column3 = ['s', 15]
        column1.extend(column2) #Attaches column1 and 2
        column1.extend(column3)
        df.loc[i]=np.array(column1) #Adds row to dataframe
        os.chdir(rootdir) #Goes back to the parent directory
        print os.getcwd() #Debug -- check if the directory has been changed
        i=i+1 #Increment counter
    print df #Print final dataframe
    writer = pd.ExcelWriter('output.xlsx') #Write excel output
    df.to_excel(writer,'Sheet1')
    writer.save()
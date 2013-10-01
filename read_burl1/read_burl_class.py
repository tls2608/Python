##############################################################################
#
#This file contains a class that will read in the time, pressure, wind speed, 
#and wind direction for a given bouy data .dat file
#
#The data is stored in a local dictionary (data) and passed to the global 
#variable (data.data) and printed 
#
##############################################################################
#
#Created by: Taylor Sansom
#September 11, 2013
#
##############################################################################

import numpy as np
import datetime as dt

class getdata_c():
    
    def __init__(self, file):
        
        self.file=file
    
        f=open(self.file)
    
        pres = []
        wspd = []
        wdir = []
        date = []
        u_wind = []
        v_wind = []
    
        for line in f.readlines()[2:]:
            data = line.split()
            pres.append( float(data[12]) )
            wdir.append( float(data[5]) * np.pi/180 )
            wspd.append( float(data[6]) )
            date.append( str(data[0] + data[1] + data[2] + data[3] +  data[4]) )
            
        pres = np.array(pres)
        wdir = np.array(wdir)
        wspd = np.array(wspd)
        date = np.array(date)
        
        u_wind = -wspd * np.sin(wdir)
        v_wind = -wspd * np.cos(wdir)
                
        date = [ dt.datetime.strptime(date[x], "%Y%m%d%H%M") for x in range(len(date)) ]
        
        self.data={'date': np.array(date), 'u_wind': np.array(u_wind), 'v_wind': np.array(v_wind), 'pres': np.array(pres)}
        
    def __repr__(self):
        return self.data
            
        
data=getdata_c('burl1_2011.dat')

print data.data

##############################################################################
#
#read_usgsdata.py
#
###############################################################################
#
#This script will read discharge data from the USGS url and plot a specified
#time series based on user inputs. The mean and standard deviation is 
#calculated based on all the data read in. The plot includes the annual daily 
#mean of the time series (red), +-1 standard deviation boundaries (orange) and 
#actual daily discharge over the top (blue).
#
###############################################################################
#
#Inputs: 8-digit station id number, beginning year and ending year for plotting
#
###############################################################################
#
#Created by: Taylor Sansom
#Department of Atmospheric Science
#Texas A&M University
#
###############################################################################

import numpy as np
import urllib as ul
import datetime as dt
from pylab import *

site=raw_input("Enter site number: ")

file = ul.urlopen(' http://waterdata.usgs.gov/nwis/dv?cb_00060=on&format=rdb&begin_date=1900-09-23&end_date=2013-09-23&site_no='+site)

#Initialization of variables
date = []
cb = []
calc = [[],[0.]*366,[0]*366,[0.]*366,[],[0.]*366,[],[]]
#calc[0] is a date string for matching dates
#calc[1] is the sum for all iterations
#calc[2] is the count of itereations
#calc[3] is the mean
#calc[4] is a list of all entries
#calc[5] is the standard deviation
#calc[6] is the upper bound
#calc[7] is the lower bound
avg = []
upper = []
lower = []

#Reading in all data
for line in file.readlines()[28:]:
    data = line.split()
    date.append( dt.datetime.strptime(str(data[2]), '%Y-%m-%d').date() )
    cb.append( float(data[3])/35.315 )

#This creates a list of every day in a leap year for comparison purposes
d1, d2 = dt.date(2000, 1, 1), dt.date(2000, 12, 31)
delta = d2 - d1

for i in range(delta.days + 1):
    calc[0].append(str(d1 + dt.timedelta(days=i))[5:10])
    calc[4].append([])

#This section partitions the data by day by comparing the strings of dates,
#adding the discharge value to the sum and counting the entries for each day
for i in range(len(date)):
    idx = calc[0].index(str(date[i])[5:10])
    calc[1][idx] = calc[1][idx] + cb[i]
    calc[2][idx] = calc[2][idx] + 1
    calc[4][idx].append(cb[i])

#This calculates the mean, standard deviation and upper/lower bounds for one
#standard deviation from mean
for i in range(len(calc[0])):
    calc[3][i] = calc[1][i] / calc[2][i]
    calc[5][i] = np.std(calc[4][i])
    calc[6].append(calc[3][i]+calc[5][i])
    calc[7].append(calc[3][i]-calc[5][i])
    if calc[7][i] < 0:
        calc[7][i] = 0

#This section takes user input for plot time limits
yr1 = dt.datetime(int(raw_input("Enter beginning year: ")),1,1).date()
yr2 = dt.datetime(int(raw_input("Enter ending year: ")),12,31).date()
yrs = yr2.year - yr1.year + 1

#This section deals with leap years
for i in range(yr1.year, yr2.year + 1):
    if i%4 != 0:
        avg = avg + calc[3][0:59] + calc[3][60:]
        upper = upper + calc[6][0:59] + calc[6][60:]
        lower = lower + calc[7][0:59] + calc[7][60:]
    else:
        avg = avg + calc[3]
        upper = upper + calc[6]
        lower = lower + calc[7]

#This line finds beginning and ending dates for plot in date list
idx1, idx2 = date.index(yr1), date.index(yr2)

#This section is for plotting the data within the user specified time limits
p1, = plot(date[idx1:idx2+1],avg,'r--')
p2, = plot(date[idx1:idx2+1],cb[idx1:idx2+1],'b',linewidth=2.0)
fill_between(date[idx1:idx2+1],upper,lower,color='orange',alpha=0.5)
ylabel('Discharge [$m^3 s^{-1}$]')
p3 = Rectangle((0, 0), 1, 1, fc = 'orange', alpha=0.5)

#This makes a different title for 1 year or many years
if yrs==1:
    title('USGS Discharge Data for Site # '+site+' for '+str(yr1)[0:4])
else:
    title('USGS Discharge Data for Site # '+site+' from '+str(yr1)[0:4]+' to '+str(yr2)[0:4])

show()

legend([p1, p2, p3], ['Daily Mean', 'Daily Observations', '1$\sigma$ Bounds'])


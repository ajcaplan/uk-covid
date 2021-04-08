from datetime import datetime
start = datetime.now()

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
from pandas import read_csv
from tqdm import tqdm

from matplotlib.backends.backend_pdf import PdfPages
pp = PdfPages('COVID-19 Graphs.pdf')

print("\nGetting data from api.coronavirus.data.gov.uk...")
data = read_csv("https://api.coronavirus.data.gov.uk/v2/data?areaType=overview&metric=newCasesBySpecimenDateAgeDemographics&format=csv").values.tolist()

# Get the different age ranges used in the data
print("Getting age range...")
ages = []
for i in data[0:25]:
    if i[5] not in ages and i[5] not in ["00_59", "60+", "unassigned"]:
            ages.append(i[5])

# Create empty list entries for each age range in a dictionarys
sortage = {}
for i in ages:
    sortage[i] = []

# Populate empty lists with rates for that age
print("Dividing data into ages...")
for i in data[:len(data)-1]:
    for t in ages:
        try:
            if i[5] == t:
                sortage[t].append(float(i[7]))
        except:
            pass
        
# Generate date axis
print("Extracting dates...")
dates = []
for i in data[::len(ages)-1]:
    if i[0] not in dates:
        dates.append(i[0])
dates = dates[::-1]

for i in dates:
    tmp = i.split("-")[::-1]
    refmat = ""
    for t in tmp:
        refmat += t + "/"
    dates[dates.index(i)] = refmat[:-1]

# Group by 10 years
print("Grouping data into 10-year ranges...")
range10 = {}
for i in ages[::2]:
    if ages.index(i) != len(ages)-1:
        theNext = ages[ages.index(i)+1]
        avgd = []
        index = 0
        for t in range(len(sortage[i])):
            avgd.append((sortage[i][index] + sortage[theNext][index])/2)
            index += 1
        range10[i[0:2] + " - " + theNext[-2:]] = avgd
    else:
        range10[i] = sortage[i]

for i in range10:
    range10[i] = range10[i][::-1]
    
print("Plotting...")
fig3, ax3 = plt.subplots(figsize=(13, 7))
for i in tqdm(range10):
    try:
        ax3.plot(dates, range10[i])
    except:
        pass

print("Adjusting graph appearance...")
#ax3.xaxis.set_major_locator(mdates.DayLocator(interval=1))
#plt.rcParams["font.family"] = "Arial"
plt.xlim(left="01/03/2021", right=dates[::-1][0])
plt.xticks(rotation='vertical')

plt.ylim(bottom=0, top=100)
plt.ylabel("Rolling Case Rate")
plt.yticks(np.arange(0, 101, 10))

plt.title("Recent Averaged Case Rate by Age Group", pad=15)
plt.axvline(x="08/03/2021", color="black")
ax3.tick_params(top=True, right=True)
ax3.legend([i for i in range10], bbox_to_anchor=(1.01, 1))
#plt.text(0.85, 1.035, credit, transform = ax3.transAxes)
plt.tight_layout()
print("Saving...")
#plt.savefig("Case Rates by Age.pdf")
pp.savefig()
print("Completed. Runtime:", datetime.now() - start, "\n")

#################################################################
print("Running admissions by NHS regions")
start = datetime.now()
from math import isnan

print("\nGetting data from api.coronavirus.data.gov.uk...")
data = read_csv("https://api.coronavirus.data.gov.uk/v2/data?areaType=nhsRegion&metric=hospitalCases&metric=newAdmissionsRollingRate&format=csv").values.tolist()
data = sorted(data, key = lambda row: datetime.strptime(row[0], "%Y-%m-%d"), reverse=True)
# Get the different age ranges used in the data
print("Getting trust names...")
trusts = []
for i in data[0:]:
    if i[3] not in trusts:
            trusts.append(i[3])

# Create empty list entries for each age range in a dictionarys
sortage = {}
dates = {}
for i in trusts:
    sortage[i] = []
    dates[i] = []

# Populate empty lists with rates for that age
print("Dividing data into trusts...")
for i in data[:len(data)-1]:
    for t in trusts:
        try:
            if i[3] == t:
                sortage[t].append(float(i[5]))
                if i[0] not in dates[t]:
                    dates[t].append(i[0])
        except:
            pass
        
for i in sortage:
    sortage[i] = sortage[i][::-1]
    index = 0
    for t in sortage[i]:
        if isnan(t):
            sortage[i][index] = sortage[i][index-1]
        index += 1

print("Extracting and ordering dates...")
for t in dates:
    dates[t] = dates[t][::-1]
    for i in dates[t]:
        tmp = i.split("-")[::-1]
        refmat = ""
        for j in tmp:
            refmat += j + "/"
        dates[t][dates[t].index(i)] = refmat[:-1]

#for i in dates:
#    dates[i].sort(key=lambda date: datetime.strptime(date, "%d/%m/%Y"))

print("Plotting...")
fig, ax = plt.subplots(figsize=(14, 7))
for i in tqdm(sortage):
    try:
        ax.plot(dates[i][8:], sortage[i][8:])
    except:
        print("passing", i)

print("Adjusting graph appearance...")
#plt.xticks(ticks = dates["London"][::30], labels = dates["London"][::30])
ax.xaxis.set_major_locator(mdates.MonthLocator(interval=1))
#plt.rcParams["font.family"] = "Arial"
plt.xlim(left=dates["London"][8], right=dates["London"][-6])

plt.ylim(bottom=0, top=70)
ax.legend([i for i in sortage], bbox_to_anchor=(1.225, 1))
plt.ylabel("Rolling Rate")
plt.xticks(rotation='vertical')

plt.title("Hospital Admissions by NHS Region", pad=15)
ax.tick_params(top=True, right=True)
#plt.text(0.91, 1.035, credit, transform = ax.transAxes)
plt.tight_layout()
print("Saving...")
#plt.savefig("Hospital Admissions by NHS Region.pdf")
pp.savefig()
print("Plotting recent data...")
fig2, ax2 = plt.subplots(figsize=(13, 7))
for i in tqdm(sortage):
    try:
        ax2.plot(dates[i][-30:-3], sortage[i][-30:-3])
    except:
        print("passing", i)

print("Adjusting graph appearance...")
plt.title("Recent Hospital Admissions by NHS Region", pad=15)
plt.ylabel("Rolling Rate")
ax2.tick_params(top=True, right=True)
plt.xticks(rotation='vertical')
ax2.xaxis.set_major_locator(mdates.DayLocator(interval=1))
plt.ylim(bottom=0, top=10)
ax2.legend([i for i in sortage])
plt.xlim(left=dates["London"][-30], right=dates["London"][-4])
#plt.text(0.77, 1.002, credit, transform = ax.transAxes)
plt.tight_layout()
#plt.savefig("Recent Hospital Admissions by NHS Region.pdf")
print("Completed. Runtime:", datetime.now() - start, "\n")

pp.savefig()
pp.close()

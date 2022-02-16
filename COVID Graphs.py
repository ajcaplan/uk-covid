from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
from pandas import read_csv
from tqdm import tqdm
from matplotlib.backends.backend_pdf import PdfPages
from math import isnan

pp = PdfPages('COVID-19 Graphs.pdf')

#################################################################

print("Running admissions by NHS regions")
print("\nGetting data from api.coronavirus.data.gov.uk...")
data = read_csv("https://api.coronavirus.data.gov.uk/v2/data?areaType=nhsRegion&metric=hospitalCases&metric=newAdmissionsRollingRate&format=csv").values.tolist()
data = sorted(data, key = lambda row: datetime.strptime(row[3], "%Y-%m-%d"), reverse=True)

# Get the different age ranges used in the data
print("Getting region names...")
trusts = []
for i in data[0:]:
    if i[1] not in trusts:
            trusts.append(i[1])

# Create empty list entries for each age range in a dictionarys
sortage = {}
dates = {}
for i in trusts:
    sortage[i] = []
    dates[i] = []

# Populate empty lists with rates for that age
print("Dividing data into regions...")
for i in data[:len(data)-1]:
    for t in trusts:
        try:
            if i[1] == t:
                sortage[t].append(float(i[5]))
                if i[3] not in dates[t]:
                    dates[t].append(i[3])
        except:
            pass

print("Cleaning and formatting data...")
for i in sortage:
    index = 0
    for t in sortage[i][0:10]:
        if isnan(t):
            sortage[i] = sortage[i][index+1:]
            dates[i] = dates[i][index+1:]
        index += 1
    sortage[i] = sortage[i][::-1]
    dates[i] = dates[i][::-1]
    
for t in dates:
    for i in dates[t]:
        tmp = i.split("-")[::-1]
        refmat = ""
        for j in tmp:
            refmat += j + "/"
        dates[t][dates[t].index(i)] = refmat[:-1]

for i in dates: # Equalise lengths of lists
    index = dates[i].index("25/03/2020")
    dates[i] = dates[i][index:]
    sortage[i] = sortage[i][index:]

print("Plotting...")
fig, ax = plt.subplots(figsize=(14, 7))
for i in tqdm(sortage):
    ax.plot(dates[i][0:], sortage[i][0:])

print("Adjusting graph appearance...")
#plt.xticks(ticks = dates["London"][::30], labels = dates["London"][::30])
ax.xaxis.set_major_locator(mdates.MonthLocator(interval=1))
plt.xlim(left = dates["London"][0], right = dates["London"][-1])

plt.ylim(bottom=0, top=70)
ax.legend([i for i in sortage])#, bbox_to_anchor=(1.225, 1))
plt.ylabel("Rolling Rate")
plt.xticks(rotation='vertical')

plt.title("Hospital Admissions by NHS Region", pad=15)
plt.grid(axis="y", alpha=0.4)
ax.tick_params(top=True, right=True)
plt.tight_layout()
print("Saving...")
pp.savefig()
print("Plotting recent data...")
fig2, ax2 = plt.subplots(figsize=(14, 7))
for i in tqdm(sortage):
    try:
        ax2.plot(dates[i][-30:], sortage[i][-30:])
    except:
        print("passing", i)

maxxed = 0
for i in sortage:
    for t in sortage[i][-30:]:
        if t > maxxed:
            maxxed = t

print("Adjusting graph appearance...")
plt.title("Recent Hospital Admissions by NHS Region", pad=15)
plt.grid(axis="y", alpha=0.4)
plt.ylabel("Rolling Rate")
ax2.tick_params(top=True, right=True)
plt.xticks(rotation='vertical')
#ax2.xaxis.set_major_locator(mdates.DayLocator(interval=2))
plt.ylim(bottom=0, top=maxxed)
plt.yticks(np.arange(0, maxxed+2, 2))
ax2.legend([i for i in sortage])
plt.xlim(left = dates["London"][-30], right = dates["London"][-1])
plt.tight_layout()

print("Saving...")
pp.savefig()
print("Completed.\n")

#######################################################################

print("Running Case Rates by Age...")
print("\nGetting data from api.coronavirus.data.gov.uk...")
data = read_csv("https://api.coronavirus.data.gov.uk/v2/data?areaType=nation&metric=newCasesBySpecimenDateAgeDemographics&format=csv").values.tolist()
data = sorted(data, key = lambda row: datetime.strptime(row[3], "%Y-%m-%d"), reverse=True)

# Get the different age ranges used in the data
print("Getting age range...")
ages = []
for i in data[0:25]:
    if i[4] not in ages and i[4] not in ["00_59", "60+", "unassigned"]:
            ages.append(i[4])

# Create empty list entries for each age range in a dictionarys
sortage = {}
for i in ages:
    sortage[i] = []

# Populate empty lists with rates for that age
print("Dividing data into ages...")
for i in data[:len(data)-1]:
    for t in ages:
        try:
            if i[4] == t and i[1] == "England":
                sortage[t].append(float(i[7]))
        except:
            pass
        
# Generate date axis
print("Extracting and formatting dates...")
dates = []
for i in data[::len(ages)-1]:
    if i[3] not in dates:
        dates.append(i[3])
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
fig3, ax5 = plt.subplots(figsize=(14, 7))
for i in tqdm(range10):
    ax5.plot(dates, range10[i])
ax5.xaxis.set_major_locator(mdates.MonthLocator(interval=1))
plt.ylim(bottom = 0, top = 4000)
plt.xlim(left = "01/03/2020", right = dates[-1])
plt.title("Case Rate by Age Group", pad=15)
plt.grid(axis="y", alpha=0.4)
plt.ylabel("Rolling Rate")
ax5.tick_params(top=True, right=True)
ax5.legend([i for i in range10])# bbox_to_anchor=(1.11, 1))
plt.xticks(rotation='vertical')
plt.tight_layout()
print("Saving...")
pp.savefig()
print("Completed.\n")

maxxed = 0
for i in range10:
    for t in range10[i][-30:]:
        if t > maxxed:
            maxxed = t

print("Plotting recent data...")
fig3, ax3 = plt.subplots(figsize=(14, 7))
for i in tqdm(range10):
    ax3.plot(dates[-30:], range10[i][-30:])

print("Adjusting graph appearance...")
#ax3.xaxis.set_major_locator(mdates.DayLocator(interval=2))
plt.xlim(left=dates[-30], right=dates[::-1][0])
plt.xticks(rotation='vertical')

plt.ylim(bottom=0, top=maxxed)
plt.ylabel("Rolling Rate")
plt.yticks(np.arange(0, maxxed+201, 200))

plt.title("Recent Case Rate by Age Group", pad=15)
plt.grid(axis="y", alpha=0.4)
ax3.tick_params(top=True, right=True)
ax3.legend([i for i in range10])#, bbox_to_anchor=(1.11, 1))
plt.tight_layout()
print("Saving...")
pp.savefig()
print("Completed.\n")

###############################################################

print("Running Case Rates by Region")
print("\nGetting data from api.coronavirus.data.gov.uk...")
data = read_csv("https://api.coronavirus.data.gov.uk/v2/data?areaType=region&metric=newCasesBySpecimenDateRollingRate&format=csv").values.tolist()
data = sorted(data, key = lambda row: datetime.strptime(row[3], "%Y-%m-%d"), reverse=True)

# Get the different age ranges used in the data
print("Getting region names range...")
regions = []
for i in data[0:25]:
    if i[1] not in regions:
            regions.append(i[1])

# Create empty list entries for each age range in a dictionarys
sortage = {}
dates = {}
for i in regions:
    sortage[i] = []
    dates[i] = []

# Populate empty lists with rates for that region
print("Dividing data into regions...")
for i in data[:-1]:
    for t in regions:
        try:
            if i[1] == t:
                sortage[t].append(float(i[4]))
                dates[t].append(i[3])
        except:
            pass
        
# Generate date axis
print("Formatting dates...")
for i in regions:
    dates[i] = dates[i][::-1]
    sortage[i] = sortage[i][::-1]

for t in dates:
    for i in dates[t]:
        tmp = i.split("-")[::-1]
        refmat = ""
        for j in tmp:
            refmat += j + "/"
        dates[t][dates[t].index(i)] = refmat[:-1]


print("Plotting...")
fig4, ax6 = plt.subplots(figsize=(14, 7))
for i in tqdm(sortage):
    try:
        ax6.plot(dates[i], sortage[i])
    except:
        print(i)
        
#ax6.xaxis.set_major_locator(mdates.MonthLocator(interval=1))
plt.xticks(ticks = dates["London"][19::30], labels = dates["London"][19::30])
plt.ylim(bottom = 0, top = 3500)
plt.xlim(left = "15/03/2020", right = dates["London"][-1])
plt.title("Case Rate by Region", pad=15)
plt.grid(axis="y", alpha=0.4)
plt.ylabel("Rolling Rate")
ax6.tick_params(top=True, right=True)
ax6.legend([i for i in sortage])
plt.xticks(rotation='vertical')
plt.tight_layout()
print("Saving...")
pp.savefig()
print("Completed.\n")

print("Plotting recent data...")
maxxed = 0
for i in sortage:
    for t in sortage[i][-30:]:
        if t > maxxed:
            maxxed = t
        
fig5, ax7 = plt.subplots(figsize=(14, 7))
for i in tqdm(sortage):
    ax7.plot(dates[i][-30:], sortage[i][-30:])

print("Adjusting graph appearance...")
plt.xlim(left=dates["London"][-30], right=dates["London"][-1])
plt.xticks(rotation='vertical')

plt.ylim(bottom=0, top=maxxed)
plt.ylabel("Rolling Rate")
plt.yticks(np.arange(0, maxxed + 201, 200))

plt.title("Recent Case Rate by Region", pad=15)
plt.grid(axis="y", alpha=0.4)
ax7.tick_params(top=True, right=True)
ax7.legend([i for i in sortage])#, bbox_to_anchor=(1.11, 1))
plt.tight_layout()
print("Saving...")
pp.savefig()
print("Completed.\n")

###############################################################

print("Running R-Number...")

print("\nGetting data from api.coronavirus.data.gov.uk...")
data = read_csv("https://api.coronavirus.data.gov.uk/v2/data?areaType=nhsRegion&metric=transmissionRateMin&metric=transmissionRateMax&format=csv").values.tolist()
data = sorted(data, key = lambda row: datetime.strptime(row[3], "%Y-%m-%d"), reverse=True)
for i in data:
    i.append(0.5*(i[4]+i[5]))


# Get the different regions used in the data
print("Getting region names...")
regions = []
for i in data:
    if i[1] not in regions:
            regions.append(i[1])

# Create empty list entries for each region in a dictionary
sortage = {}
dates = {}
for i in regions:
    sortage[i] = []
    dates[i] = []

# Populate empty lists with rates for that region
print("Dividing data into trusts...")
absmin = 1 # These used to adjust graph's y-axis scale
absmax = 1
for i in data:
    for t in regions:
        if i[1] == t:
            sortage[t].append(i[6])
            if i[6] < absmin:
                absmin = i[6]
            if i[6] > absmax:
                absmax = i[6]
            if i[3] not in dates[t]:
                dates[t].append(i[3])

absmin = round(absmin, 1)
absmax = round(absmax, 1)

print("Cleaning and formatting data...")
for i in sortage:
    sortage[i] = sortage[i][::-1]
    dates[i] = dates[i][::-1]

for t in dates:
    for i in dates[t]:
        tmp = i.split("-")[::-1]
        refmat = ""
        for j in tmp:
            refmat += j + "/"
        dates[t][dates[t].index(i)] = refmat[:-1]

print("Plotting...")
fig, ax4 = plt.subplots(figsize=(14, 7))
for i in tqdm(sortage):
    ax4.plot(dates[i], sortage[i], alpha=0.7)

print("Adjusting graph appearance...")
plt.xticks(ticks = dates["London"][::2], labels = dates["London"][::2])
plt.xlim(left = dates["London"][0], right = dates["London"][-1])
plt.ylabel("Transmission rate")
plt.xticks(rotation='vertical')
plt.ylim(bottom = absmin - 0.1, top = absmax + 0.1)
plt.yticks(np.arange(absmin - 0.1, absmax + 0.15, 0.2))

ax4.legend([i for i in sortage])#, bbox_to_anchor=(1.225, 1))
plt.hlines(1.0, dates["London"][0], dates["London"][-1], colors = "black", linestyles = "dotted")
plt.title("Transmission Rates by NHS Region", pad=15)
plt.grid(axis="y", alpha=0.4)
ax4.tick_params(top=True, right=True)
plt.tight_layout()
print("Saving...")
pp.savefig()
print("Completed.\n")

pp.close()

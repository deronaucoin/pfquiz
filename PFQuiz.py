#
#Created by: Deron Aucoin, dlayne76@gmail.com
#Date: 2/5/2013
#Purpose: This is an interview assignment script that reads the contents of several CSV files, 
#merges records across the files and summarizes in a single CSV output

import os, re, csv
from numpy import tile, zeros

def getClosestProviders(controlRecord, treatments):
    size = treatments.shape[0]
    differences = tile(controlRecord, (size,1)) - treatments
    diffsquared = differences**2
    distancessquared = diffsquared.sum(axis=1)
    distances = distancessquared**0.5 # take square root
    sorted = distances.argsort()
    return sorted, distances

savedCSVFile = 'Summary.csv'
f = open(savedCSVFile, 'wb')
writer = csv.writer(f)
writer.writerow(['ProviderId','MatchedProviderId','FileNo'])

for dirname, dirnames, filenames in os.walk('data'):

        for filename in filenames:
            path = os.path.join(dirname, filename)
            fileNum = re.search('\d{1,2}',filename).group()
            print "Opening", path, "file # ", fileNum
            control = []
            fullTreatmentMatrix = zeros((200,4))
            i = 0
            with open(path, 'rb') as csvfile:
                reader = csv.reader(csvfile)
                next(reader)
                for row in reader:
                    row = [int(x) for x in row]
                    if row[4] == 1:
                        #print row
                        fullTreatmentMatrix[i,:]= row[0:4]
                        i += 1
                    if row[4]== 0:
                        control.append(row[0:4])
       
            for cprovider in control:           
                sorted, distances = getClosestProviders(cprovider[1:4],fullTreatmentMatrix[:,1:4])
                if distances[sorted[0]] != distances[sorted[0+1]]:
                    matchedProviderId = sorted[0]+1
                    writer.writerow([cprovider[0],matchedProviderId,int(fileNum)])
                    
f.close()
print "Results saved to", savedCSVFile

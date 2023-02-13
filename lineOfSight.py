import numpy as np

# purpose: calculate the coordinate range around the binary to determine local population density of secondary stars
# inputs coordinates of a binary and distance (in arcminutes)
# outputs an array of [minRA, maxRA, minDec, maxDec] in decimal degrees
def calcCoordRange(binRA, binDec, dist):
    # convert arcminutes to decimal degrees
    distDeg = dist/60.
    # calcualte min and max RA and Dec values
    minRA = binRA - (distDeg) * np.cos(np.radians(binDec))
    maxRA = binRA + (distDeg) * np.cos(np.radians(binDec))
    decA = binDec - distDeg
    decB = binDec + distDeg
    # confusing because sometimes Dec is negative ...
    if decA < decB:
        minDec = decA
        maxDec = decB
    else:
        minDec = decB
        maxDec = decA
    return [minRA,maxRA,minDec,maxDec]

# purpose: selects secondary stars within coordinate range
# inputs an array of min/max RA and Dec values
# outputs an array of the coordiantes (in decimal degrees) of all of the secondary stars within the region
def selectSecondaries(secondaries, coordRange):
    selectedSecondaries = secondaries[(secondaries[:,0] > coordRange[0]) &
                                      (secondaries[:,0] < coordRange[1]) &
                                      (secondaries[:,1] > coordRange[2]) &
                                      (secondaries[:,1] < coordRange[3])]
    return selectedSecondaries

# purpose: calculates the distance between an object and list of objects
# inputs coordiantes (decimal degrees) of fake star and list of real secondaries
# outputs the distance in degrees (as an array)
# assumption: given the small distances, this does not use spherical trig
def calcDist(starA,starB):
    RAarr = np.ones(len(starB))*starA[0]
    Decarr = np.ones(len(starB))*starA[1]
    return np.sqrt(((RAarr-starB[:,0])*np.cos(np.radians(starA[1])))**2.+(Decarr-starB[:,1])**2.)

# purpose: determines the percentage of line-of-sight stars
# inputs coordinate range, array of secondaries in the region, number of runs, distance for LOS
# outputs the percentage of the populated stars that will have LOS companions
def calcLOS (coordRange, secondaries, nRuns, distLOS):
    # counter that increments if there is a line-of-sight binary
    los = 0

    # loop through the number of runs
    for i in range(0,nRuns):
        # generate random RA and Dec values within the coordinate range
        raRand = np.random.uniform(coordRange[0],coordRange[1])
        decRand = np.random.uniform(coordRange[2],coordRange[3])

        # calculate the distance between this fake star and each of the secondaries
        # convert to arcseconds
        dists = calcDist([raRand,decRand],secondaries)*3600.

        # if there is a distance less than the distLOS, increment the LOS counter
        if len(dists) > 0:
            if min(dists) < distLOS:
                los = los + 1
                
    # return the percentage of line-of-sight binaries
    return los*1.0/nRuns

# purpose: determines the overall line-of-sight percentage
# inputs:
#  - nRuns: number of runs for MC
#  - distLOS: distance between objects needed for "line-of-sight" classification (arcseconds)
#  - distSurvey: distance around object for population density (arcminutes)
#  - unknownBinaries: list of objects as a numpy array with the first colum as RA, second as Dec (decimal degree)
#  - secondaries: list of objects as a numpy array with the first colum as RA, second as Dec (decimal degree)

def calcLOSpercent(nRuns, distLOS, distSurvey, unknownBinaries, secondaries):
    # create empty array of percentage of LOS results
    losResults = np.zeros(len(unknownBinaries))

    # loop through all unknown Binaries
    for i in range(0,len(unknownBinaries)):
        # calculate coordiante range
        coordRange = calcCoordRange(unknownBinaries[i,0],unknownBinaries[i,1],distSurvey)
        # select the secondary objects within that range
        selectedSecondaries = selectSecondaries(secondaries, coordRange)
        # calculate percentage of LOS binaries
        losCalc = calcLOS(coordRange,selectedSecondaries,nRuns,distLOS)
        # save in array to be returned at the end
        losResults[i] = losCalc

    np.savetxt("losResults.csv",losResults,delimiter=",")
    return losResults

def main():
    nRuns = 10000
    distLOS = 0.75 # arcseconds
    distSurvey = 5 # arcminutes
    unknownBinaries = np.loadtxt("M31binaries.csv",delimiter=",")
    secondaries = np.loadtxt("M31OBs.csv",delimiter=",")
    losResults = calcLOSpercent(nRuns, distLOS, distSurvey, unknownBinaries, secondaries)
    
if __name__ == "__main__":
    main()

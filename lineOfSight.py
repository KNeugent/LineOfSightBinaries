import numpy as np


def calcCoordRange(binRA, binDec, dist):
    """
    Calculates the maximum and minimum RA and Dec values around an object
    given a distance.

         Parameters:
              binRA (float): RA of binary in decimal degrees
              binDec (float): Declination of binary in decimal degrees
              dist (float): distance from binary in arcminutes

         Returns:
              coordRange ([float,float,float,float]): minimum RA, maximum RA, minimum Dec,
                                                      maximum Dec in decimal degrees
    """
    # convert arcminutes to decimal degrees
    distDeg = dist / 60.0

    # calculate min and max RA and Dec values
    # convert to radians to use numpy cos
    minRA = binRA - (distDeg) * np.cos(np.radians(binDec))
    maxRA = binRA + (distDeg) * np.cos(np.radians(binDec))
    decA = binDec - distDeg
    decB = binDec + distDeg

    # necessary because sometimes the Dec is negative
    if decA < decB:
        minDec = decA
        maxDec = decB
    else:
        minDec = decB
        maxDec = decA

    coordRange = [minRA, maxRA, minDec, maxDec]
    return coordRange


def selectSecondaries(secondaries, coordRange):
    """
    Returns the subset of secondaries that are within the given coordinate range

         Parameters:
              secondaries ([float,float]): coordinates of secondaries [RA, Dec] in decimal degrees
              coordRange ([float,float,float,float]): minimum RA, maximum RA, minimum Dec,
                                                      maximum Dec in decimal degrees

         Returns:
              selectedSecondaries ([float,float]): coordinates of secondaries [RA, Dec] in decimal degrees

    """
    selectedSecondaries = secondaries[
        (secondaries[:, 0] > coordRange[0])
        & (secondaries[:, 0] < coordRange[1])
        & (secondaries[:, 1] > coordRange[2])
        & (secondaries[:, 1] < coordRange[3])
    ]
    return selectedSecondaries


def calcDist(starA, stars):
    """
    Calculates the distance between a single object and a list of objects

         Parameters:
              starA (float,float): RA and Dec in decimal degrees
              stars ([float,float]): array of RA and Dec in decimal degrees

         Returns:
              distVals ([float]): distances in decimal degrees
    """
    RAarr = np.ones(len(stars)) * starA[0]
    Decarr = np.ones(len(stars)) * starA[1]
    # assumption: given the small distances, this does not use spherical trig
    distVals = np.sqrt(
        ((RAarr - stars[:, 0]) * np.cos(np.radians(starA[1]))) ** 2.0
        + (Decarr - stars[:, 1]) ** 2.0
    )

    return distVals


def calcLOS(coordRange, secondaries, nRuns, distLOS):
    """
    Determines the percentage chance that a star is a line-of-sight binary

         Parameters:
              coordRange ([float,float,float,float]): minimum RA, maximum RA, minimum Dec,
                                                      maximum Dec in decimal degrees
              secondaries ([float,float]): coordinates of secondaries [RA, Dec] in decimal degrees
              nRuns (int): number of Monte Carlo simulations
              distLOS (float): separation between two objects (in arcminutes)
                             necessary to be a line-of-sight companion

         Returns:
              losPercent (float): percent of runs that had a line-of-sight companion
    """

    # counter that increments if there is a line-of-sight binary
    los = 0

    # loop through the number of runs
    for i in range(0, nRuns):
        # generate random RA and Dec values within the coordinate range
        raRand = np.random.uniform(coordRange[0], coordRange[1])
        decRand = np.random.uniform(coordRange[2], coordRange[3])

        # calculate the distance between this fake star and each of the secondaries
        # convert to arcseconds
        dists = calcDist([raRand, decRand], secondaries) * 3600.0

        # if there is a distance less than the distLOS, increment the LOS counter
        if len(dists) > 0:
            if min(dists) < distLOS:
                los = los + 1

    # return the percentage of line-of-sight binaries
    # multiply by 1.0 to convert to float
    losPercent = los * 1.0 / nRuns
    return losPercent


def calcLOSpercent(nRuns, distLOS, distSurvey, unknownBinaries, secondaries):
    """
    Determines the line-of-sight percentage for each star

         Parameters:
              nRuns (int): number of Monte Carlo simulations
              distLOS (float): separation between two objects (in arcminutes)
                             necessary to be a line-of-sight companion
              distSurvey (float): distance around object for population density in arcminutes
              unknownBinaries ([float,float]): coordinates of unknown binaries [RA, Dec] in decimal degrees
              secondaries ([float,float]): coordinates of secondaries [RA, Dec] in decimal degrees

         Returns:
              losResults ([float]): one value for each star
    """
    # create empty array of percentage of LOS results
    losResults = np.zeros(len(unknownBinaries))

    # loop through all unknown Binaries
    for i in range(0, len(unknownBinaries)):
        # calculate coordiante range
        coordRange = calcCoordRange(unknownBinaries[i, 0], unknownBinaries[i, 1], distSurvey)
        # select the secondary objects within that range
        selectedSecondaries = selectSecondaries(secondaries, coordRange)
        # calculate percentage of LOS binaries
        losCalc = calcLOS(coordRange, selectedSecondaries, nRuns, distLOS)
        # save in array to be returned at the end
        losResults[i] = losCalc

    return losResults


def main():
    # Note: these have been pre-populated with test values
    # Please edit these to suit your needs
    nRuns = 10000
    distLOS = 0.75  # arcseconds
    distSurvey = 5  # arcminutes

    unknownBinaries = np.loadtxt("M31binaries.csv", delimiter=",")
    secondaries = np.loadtxt("M31OBs.csv", delimiter=",")

    losResults = calcLOSpercent(nRuns, distLOS, distSurvey, unknownBinaries, secondaries)

    np.savetxt("losResults.csv", losResults, delimiter=",")


if __name__ == "__main__":
    main()

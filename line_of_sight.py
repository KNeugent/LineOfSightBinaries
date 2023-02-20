import numpy as np


def calc_coord_range(bin_RA, bin_dec, dist):
    """
    Calculates the maximum and minimum RA and Dec values around an object
    given a distance.

         Parameters:
              bin_RA (float): RA of binary in decimal degrees
              bin_dec (float): Declination of binary in decimal degrees
              dist (float): distance from binary in arcminutes

         Returns:
              coord_range ([float,float,float,float]): minimum RA, maximum RA, minimum Dec,
                                                       maximum Dec in decimal degrees
    """
    # convert arcminutes to decimal degrees
    dist_deg = dist / 60.0

    # calculate min and max RA and Dec values
    # convert to radians to use numpy cos
    min_RA = bin_RA - (dist_deg) * np.cos(np.radians(bin_dec))
    max_RA = bin_RA + (dist_deg) * np.cos(np.radians(bin_dec))
    dec_A = bin_dec - dist_deg
    dec_B = bin_dec + dist_deg

    # necessary because sometimes the Dec is negative
    if dec_A < dec_B:
        min_dec = dec_A
        max_dec = dec_B
    else:
        min_dec = dec_B
        max_dec = dec_A

    coord_range = [min_RA, max_RA, min_dec, max_dec]
    return coord_range


def select_secondaries(secondaries, coord_range):
    """
    Returns the subset of secondaries that are within the given coordinate range

         Parameters:
              secondaries ([float,float]): coordinates of secondaries [RA, Dec] in decimal degrees
              coord_range ([float,float,float,float]): minimum RA, maximum RA, minimum Dec,
                                                       maximum Dec in decimal degrees

         Returns:
              selected_secondaries ([float,float]): coordinates of secondaries [RA, Dec] in decimal degrees

    """
    selected_secondaries = secondaries[
        (secondaries[:, 0] > coord_range[0])
        & (secondaries[:, 0] < coord_range[1])
        & (secondaries[:, 1] > coord_range[2])
        & (secondaries[:, 1] < coord_range[3])
    ]
    return selected_secondaries


def calc_dist(star_A, stars):
    """
    Calculates the distance between a single object and a list of objects

         Parameters:
              star_A (float,float): RA and Dec in decimal degrees
              stars ([float,float]): array of RA and Dec in decimal degrees

         Returns:
              dist_vals ([float]): distances in decimal degrees
    """
    RA_arr = np.ones(len(stars)) * star_A[0]
    dec_arr = np.ones(len(stars)) * star_A[1]
    # assumption: given the small distances, this does not use spherical trig
    dist_vals = np.sqrt(
        ((RA_arr - stars[:, 0]) * np.cos(np.radians(star_A[1]))) ** 2.0
        + (dec_arr - stars[:, 1]) ** 2.0
    )

    return dist_vals


def calc_LOS(coord_range, secondaries, n_runs, dist_LOS):
    """
    Determines the percentage chance that a star is a line-of-sight binary

         Parameters:
              coord_range ([float,float,float,float]): minimum RA, maximum RA, minimum Dec,
                                                      maximum Dec in decimal degrees
              secondaries ([float,float]): coordinates of secondaries [RA, Dec] in decimal degrees
              n_runs (int): number of Monte Carlo simulations
              dist_LOS (float): separation between two objects (in arcminutes)
                                necessary to be a line-of-sight companion

         Returns:
              los_percent (float): percent of runs that had a line-of-sight companion
    """

    # counter that increments if there is a line-of-sight binary
    los = 0

    # loop through the number of runs
    for i in range(0, n_runs):
        # generate random RA and Dec values within the coordinate range
        ra_rand = np.random.uniform(coord_range[0], coord_range[1])
        dec_rand = np.random.uniform(coord_range[2], coord_range[3])

        # calculate the distance between this fake star and each of the secondaries
        # convert to arcseconds
        dists = calc_dist([ra_rand, dec_rand], secondaries) * 3600.0

        # if there is a distance less than the distLOS, increment the LOS counter
        if len(dists) > 0:
            if min(dists) < dist_LOS:
                los = los + 1

    # return the percentage of line-of-sight binaries
    # multiply by 1.0 to convert to float
    los_percent = los * 1.0 / n_runs
    return los_percent


def calc_LOS_percent(n_runs, dist_LOS, dist_survey, unknown_binaries, secondaries):
    """
    Determines the line-of-sight percentage for each star

         Parameters:
              n_runs (int): number of Monte Carlo simulations
              dist_LOS (float): separation between two objects (in arcminutes)
                             necessary to be a line-of-sight companion
              dist_survey (float): distance around object for population density in arcminutes
              unknown_binaries ([float,float]): coordinates of unknown binaries [RA, Dec] in decimal degrees
              secondaries ([float,float]): coordinates of secondaries [RA, Dec] in decimal degrees

         Returns:
              los_results ([float]): one value for each star
    """
    # create empty array of percentage of LOS results
    los_results = np.zeros(len(unknown_binaries))

    # loop through all unknown Binaries
    for i in range(0, len(unknown_binaries)):
        # calculate coordiante range
        coord_range = calc_coord_range(unknown_binaries[i, 0], unknown_binaries[i, 1], dist_survey)
        # select the secondary objects within that range
        selected_secondaries = select_secondaries(secondaries, coord_range)
        # calculate percentage of LOS binaries
        los_calc = calc_LOS(coord_range, selected_secondaries, n_runs, dist_LOS)
        # save in array to be returned at the end
        los_results[i] = los_calc

    return los_results


def main():
    # Note: these have been pre-populated with test values
    # Please edit these to suit your needs
    n_runs = 10000
    dist_LOS = 0.75  # arcseconds
    dist_survey = 5  # arcminutes

    unknown_binaries = np.loadtxt("M31_binaries.csv", delimiter=",")
    secondaries = np.loadtxt("M31_OBs.csv", delimiter=",")

    los_results = calc_LOS_percent(n_runs, dist_LOS, dist_survey, unknown_binaries, secondaries)

    np.savetxt("los_results.csv", los_results, delimiter=",")


if __name__ == "__main__":
    main()

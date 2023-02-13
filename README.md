# Line of Sight Objects

This program calculates the percentage chance that two astronomical objects are in a line-of-sight binary system as opposed to a gravitationally bound system. This is done using a Monte Carlo simulation and knowledge of the local environment's population density. This example is applied to a set of red supergiant + OB binary systems in the galaxies M31, M33, and the Magellanic Clouds but can be applied to any two astronomical objects in an environment.

## Methodology
When determining whether two objects (from now on, we will assume these are stars) that are spatially close to one another in the sky are gravitationally bound as opposed to simply line-of-sight systems, it is important to look at the surrounding stellar environment. If there are relatively few other stars in the region that could be line-of-sight companions, it is more likely that the binary system is gravitationally bound. To make this determination, the program does the following:
1) Identifies a binary system.
![Step1](https://github.com/KNeugent/LineOfSightBinaries/blob/main/images/step1.jpg)
2) Draws a circle around the binary system.
![Step2](https://github.com/KNeugent/LineOfSightBinaries/blob/main/images/step2.jpg)
3) Identifies the population of secondary stars within the circle (in the example case, this would be the OB stars that are the secondary stars in the red supergiant + OB binary system).
![Step3](https://github.com/KNeugent/LineOfSightBinaries/blob/main/images/step3.jpg)
4) Randomly places the binary system at different places within the circle and determines the number of times it would be within a certain distance of the secondary stars, and thus a line-of-sight binary.

This answer will be different for the system in the field shown above (a relatively uncrowded region) compared to the field shown below (a crowded region), which is why a knowledge of the stellar population is necessary.
![Step4](https://github.com/KNeugent/LineOfSightBinaries/blob/main/images/step4.jpg)

## Using this code

### Dependencies

The only imported package is numpy. This code has been tested using python3.

### Running the code

The only values that need to be changed are located in the main method. Here you can change:
* the number of Monte Carlo simulations that will be performed
* the distance (in arcseconds) between objects when used to determine if two objects are in a light-of-sight pairing
* the distance (in arcminutes) away from the object to define as the "local environment"
* the list of unknown binaries
* the list of known secondary stars in the surrounding environment.

Example csv files are provided as well. `M31binaries.csv` is the list of unknown binaries and `M31OBs.csv` is the list of secondary stars.

The code can then be run using `python lineOfSight.py`

### Outputted files

The program outputs `losResults.csv` that shows the percentage of times each object was close enough to a secondary object such that it would be classified as a line-of-sight binary. 

## A test case: Red Supergiant + OB binaries
The example below walks us through the process of applying the Monte Carlo simulation to red supergiant + OB binaries in a few Local Group galaxies.

### Red Supergiant + OB binaries
The list of red supergiant binary systems comes from [Neugent et al. (2020)](https://ui.adsabs.harvard.edu/abs/2020ApJ...900..118N/abstract) for the Magellanic Clouds and [Neugent (2021)](https://ui.adsabs.harvard.edu/abs/2021ApJ...908...87N/abstract) for M31 and M33. 

## Selecting the OB stars
The initial list of stars within these galaxies comes from the Local Group Galaxy Survey / [Massey et al. (2006)](https://ui.adsabs.harvard.edu/abs/2006AJ....131.2478M/abstract) for M31 and M33, [Zaritsky et al. (2002)](https://ui.adsabs.harvard.edu/abs/2002AJ....123..855Z/abstract) for the Small Magellanic Cloud, and [Zaritsky et al. (2004)](https://ui.adsabs.harvard.edu/abs/2004AJ....128.1606Z/abstract) for the Large Magellanic Cloud.

To select the OB stars from these lists, we'll remove everything redder than an A0V using a (B-V) cutoff of (B-V) < 0.0.

However, we must consider reddening. From Massey et al. (2007) we get the reddening values E(B-V) for the four galaxies. The first number is the average reddening and the number in parenthesis is the range. For this project, we'll use the average.
* M31: 0.13 (0.06-0.25)
* M33: 0.12 (0.05-0.25)
* LMC: 0.13 (0.08-0.25)
* SMC: 0.09 (0.04-0.25)

We'd also like to set a brightness criteria. Based on our observing set-up, we won't detect any OB stars fainter than V = 21.

Using these cuts, we get the following number of OB stars:
* number OBs in M31 = 26762
* number OBs in M33 = 37147
* number OBs in LMC = 1261935
* number OBs in SMC = 1455267

So, clearly there shouldn't be more OBs in the MCs than in M31 or M33, but this shows the limitations of our photometry. It is more difficult to resolve individual stars in M31 and M33 because they're further away. But, this will still give a pretty good idea of the locations of the OB stars within the galaxies.

### Determining the percentage chance of line-of-sight binaries

As an example. I've included the M31binaries.csv and M31OBs.csv files that include the coordinates of the M31 red supergiant + OB binaries and known OB stars in M31, respectively (in decimal degree csv format). Running the lineOfSight.py script with the following inputs outputs the losResults.csv file.

Inputs:
* nRuns = 10000
* distLOS = 0.75 # arcseconds
* distSurvey = 5 # arcminutes
* unknownBinaries = `M31binaries.csv`
* secondaries = `M31OBs.csv`

The output is then `losResults.csv` which shows the percentage of times each M31 red supergiant + OB binary was close enough to another OB star to be deemed a line-of-sight binary. On this run of the simulation, the highest percentage was 1.2%. So, it is very unlikely that any of these objects are line-of-sight binaries!
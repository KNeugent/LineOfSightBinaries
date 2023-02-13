# Line of Sight Objects

This program calculates the likelihood that two stars are a line-of-sight binary system as opposed to a gravitationally bound system using a Monte Carlo simulation and knowledge of the local environment's stellar density. This example is applied to a set of red supergiant + OB binary systems in the galaxies M31, M33, and the Magellanic Clouds but can be applied to any two astronomical objects in an environment.

## Methodology
When determining whether two stars that are spatially close to one another in the sky are gravitationally bound as opposed to line-of-sight systems, it is important to look at the surrounding stellar environment. If there are relatively few other stars in the region that could be line-of-sight companions, it is more likely that the binary system is gravitationally bound. To make this determination, the program does the following:
1) Identifies a binary system (red supergiant + OB stars).
![Step1](https://github.com/KNeugent/LineOfSightBinaries/blob/main/images/step1.jpg)
2) Draws a circle around the binary system.
![Step2](https://github.com/KNeugent/LineOfSightBinaries/blob/main/images/step2.jpg)
3) Identifies the population of secondary stars (OB stars) within the circle.
![Step3](https://github.com/KNeugent/LineOfSightBinaries/blob/main/images/step3.jpg)
4) Randomly places the binary system at different places within the circle and determines the number of times it would be within a certain distance of the secondary stars, and thus a line-of-sight binary.

This answer will be different for the system in the field shown above (a relatively uncrowded region) compared to the field shown below (a crowded region), which is why a knowledge of the stellar population is necessary.
![Step4](https://github.com/KNeugent/LineOfSightBinaries/blob/main/images/step4.jpg)

## Inputs
The following information is needed:
- Coordinates for the list of binary systems (in the example, for the red supergiant + OB stars)
- Coordinates for a reasonably complete population of the secondary star within the local environment (in the example, for the OB stars in each galaxy)

## Example application: Red Supergiant + OB binaries
The example below walks us through the process of applying the Monte Carlo simulation to red supergiant + OB binaries in a few Local Group galaxies.

### Red Supergiant + OB binaries
The list of red supergiant binary systems comes from [Neugent et al. (2020)](https://ui.adsabs.harvard.edu/abs/2020ApJ...900..118N/abstract) for the Magellanic Clouds and [Neugent 2021](https://ui.adsabs.harvard.edu/abs/2021ApJ...908...87N/abstract) for M31 and M33. 

## Selecting the OB stars
The initial list of stars within these galaxies comes from the Local Group Galaxy Survey / [Massey et al. (2006)](https://ui.adsabs.harvard.edu/abs/2006AJ....131.2478M/abstract) for M31 and M33, [Zaritsky et al. (2002)](https://ui.adsabs.harvard.edu/abs/2002AJ....123..855Z/abstract) for the Small Magellanic Cloud, and [Zaritsky et al. (2004)](https://ui.adsabs.harvard.edu/abs/2004AJ....128.1606Z/abstract) for the Large Magellanic Cloud.

To select the OB stars from these lists, we'll remove everything redder than an A0V using a (B-V) cutoff of (B-V) < 0.0.

However, we must consider reddening. From Massey et al. (2007) we get the reddening values E(B-V) for the four galaxies. The first number is the average reddening and the number in parenthesis is the range. For this project, we'll use the average.
M31: 0.13 (0.06-0.25)
M33: 0.12 (0.05-0.25
LMC: 0.13 (0.08-0.25)
SMC: 0.09 (0.04-0.25)

We'd also like to set a brightness criteria. Based on our observing set-up, we won't detect any OB stars fainter than V = 21.

Using these cuts, we get the following number of OB stars:
number OBs in M31 = 26762
number OBs in M33 = 37147
number OBs in LMC = 1261935
number OBs in SMC = 1455267

So, clearly there shouldn't be more OBs in the MCs than in M31 or M33, but this shows the limitations of our photometry. It is more difficult to resolve individual stars in M31 and M33 because they're further away. But, this will still give a pretty good idea of the locations of the OB stars within the galaxies.

### Determining the likelihood of line-of-sight binaries
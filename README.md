# Line of Sight Objects

This program calculates the likelihood that two stars are a line-of-sight binary as opposed to a gravitationally bound system using a Monte Carlo simulation and knowledge of the local environment's stellar density. This example is applied to a set of red supergiant + OB binary systems in the galaxies M31, M33, and the Magellanic Clouds.

## Methodology
Observed binary systems that are located further away from other stars are morea likely to be gravitationally bound as opposed to light-of-sight systems. Conversely, binary systems that are found in dense clusters are more likely to be line-of-sight systems as opposed to gravitationally bound. To estimate the likelihood that a binary system is gravitationally bound, the program takes the following steps:
1) Identify a binary system (red supergiant + OB star).
![Step1](https://github.com/KNeugent/LineOfSightBinaries/blob/main/images/step1.jpg)
2) Draw a circle around the binary system.
![Step2](https://github.com/KNeugent/LineOfSightBinaries/blob/main/images/step2.jpg)
3) Identify the population of secondary stars (OB stars) within the circle.
![Step3](https://github.com/KNeugent/LineOfSightBinaries/blob/main/images/step3.jpg)
4) Randomly place the binary system at different places within the circle and determine the number of times it would be within a certain distance of the secondary stars and thus a line-of-sight binary.

This answer will be different for the system in the field shown above compared to the field shown below, which is why a knowledge of the stellar population is necessary.
![Step4](https://github.com/KNeugent/LineOfSightBinaries/blob/main/images/step4.jpg)

## Inputs
The following information is needed:
- Coordinates for the list of binary systems (red supergiant + OB stars)
- Coordinates for a reasonably complete population of the secondary star within the local environment (OB stars in each galaxy)

## Assumptions

## Notes specific to the red supergiant + OB star use case

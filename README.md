# Line of Sight Objects

This program calculates the likelihood that two stars are a line-of-sight binary system as opposed to a gravitationally bound system using a Monte Carlo simulation and knowledge of the local environment's stellar density. This example is applied to a set of red supergiant + OB binary systems in the galaxies M31, M33, and the Magellanic Clouds but can be applied to any two astronomical objects in an environment.

## Methodology
When determining whether two stars that are spatially close to one another in the sky are gravitationally bound as opposed to line-of-sight systems, it is important to look at the surrounding stellar environment. If there are relatively few other stars in the region that could be line-of-sight companions, it is more likely that the binary system is gravitationally bound. To make this determination, the program does the following:
1) Identifies a binary system (red supergiant + OB star).
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
- Coordinates for the list of binary systems (in the above example, for the red supergiant + OB stars)
- Coordinates for a reasonably complete population of the secondary star within the local environment (in the example above, for the OB stars in each galaxy)
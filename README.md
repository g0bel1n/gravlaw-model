# Gravity Law Model Applied to inter-citis traffic

[![Python application](https://github.com/iSab01/gravlaw-model/actions/workflows/python-app.yml/badge.svg)](https://github.com/iSab01/gravlaw-model/actions/workflows/python-app.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Visualization of [this paper](https://arxiv.org/abs/0710.1274)

>**Abstract** : 
*We investigate the traffic flows of the Korean highway system, which contains both public and private transportation information. We find that the traffic flow T(ij) between city i and j forms a gravity model, the metaphor of physical gravity as described in Newton's law of gravity, P(i)P(j)/r(ij)^2, where P(i) represents the population of city i and r(ij) the distance between cities i and j. It is also shown that the highway network has a heavy tail even though the road network is a rather uniform and homogeneous one. Compared to the highway network, air and public ground transportation establish inhomogeneous systems and have power-law behaviors.* by Woo-Sung Jung, Fengzhong Wang, H. Eugene Stanley


## Demonstration

![plot](https://github.com/iSab01/gravlaw-model/blob/master/ressources/GravLawModel_France.png)

In blue, we can see the actual average traffic per day. In black we have the estimated traffic. Please aknowledge the fact that the precise value is not the point of the simualtion. The goal is to examine **tendancies** to check if the model might be close to reality. Moreover, for visualization puroposes, the width of the black ligne is not proportionnal to the real flow, but to T[i,j]^(0,7). The purpose of such a non-linear transformation is to avoid having massive flows covering the image or the inverse, not seeing any small-medium flows.

## OnBoarding

After making sure that your environnement check out the requirements, you can use the following commands :

```python

from gravLawModel import GravLawModel

model = GravLawModel(country="your_country_name", iso_a3="your_country_isoa3_code")
model.flow_calculate()
model.save()

```

For now, real values are only available for France, but you can easily modify the code to plot those of another country, if you know where to find them of course. 

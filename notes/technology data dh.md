## DH technology data

### Fuel

The fuel of each generator is based on the largest type of fuel consumed in 2020, as stated in EPC. Generators without fuel consumption are not included in the analysis.

- Boilers have a clear main fuel, with shares (>95%).
- CHPs are also usually dominated by one source (> 85%). However, the following assumptions are made:
  - ARC         : 66% municipal waste, 33% wood-waste. Municipal waste is assumed to be the main fuel.
  - KKV7        : No information on main fuel, but [VEKS](https://www.veks.dk/en/focus/kkv) states that it is a wood-chip boiler.

### Firing capacity

This data is obtained from the Energy Producer Census 2020. Non-CHP generators are aggregated based on fuel for boilers, and based on technology type for heat pumps and excess heat.

- HCV7: The stated 200 MW firing capacity is correct, given its operation has been restricted ([source](https://dma.mst.dk/vis-sag/1352675)).

### Heating and electric capacities

This data is obtained from the Energy Producer Census 2020. However, it is not used further in the analysis.

### CHP configuration
The configuration of the all cogeneration plants, excluding AMV4, is based on [Ommen et al, 2016](http://dx.doi.org/10.1016/j.energy.2015.10.063). This indicates back-pressure/extraction configuration, the option for turbine bypass, and priority access.

AMV4's configuration is taken from [Varmeplan Hovedstaden](https://varmeplanhovedstaden.dk/) and [HOFOR website](https://www.hofor.dk/baeredygtige-byer/fremtidens-fjernvarme/amagervaerket/blok-4-paa-amagervaerket/tekniske-facts-blok4/).


### Technical parameters

Technical parameters are obtained from different sources depending on the type of generator.

#### Boilers
Technical parameters (heating efficiency, VO&M and ramping) are taken from the [Technology Catalogue - Generation](https://ens.dk/en/our-services/projections-and-models/technology-data/technology-data-generation-electricity-and). The following spreadsheets are used:

- HOB_BG: 44 DH boiler, gas fired
- HOB_EL: 41 electric boiler, large
- HOB_FO: 44 DH boiler, gas fired
- HOB_GO: 44 DH boiler, gas fired
- HOB_NG: 44 DH boiler, gas fired
- HOB_WP: 09b Wood Pellets HOP
- HOP_WW: 09a Wood Pellets HOP

#### Heat Pumps
Technical parameters (VO&M and ramping) are taken from the [Technology Catalogue - Generation](https://ens.dk/en/our-services/projections-and-models/technology-data/technology-data-generation-electricity-and). 
- HP    : 40 - Comp. hp, airsource 3 MW
 
The heating efficiency is variable and calculated based on the methodology therein presented. The following temperatures are used:
- Copenhagen's air temperatures, with 5 °C increase.
- DH temperatures indicated in the manuscript.

#### Excess heat
The following parameters are assumed:
- Heating efficiency is assumed to 1, i.e., all heat is delivered to the DH network.
- VO&M is assumed to be 0 €/MW~h~.
- Ramping factor is assumed to be 1.

#### Back-pressure units

Total and electric efficiencies are obtained from [Ommen et al, 2016](http://dx.doi.org/10.1016/j.energy.2015.10.063) for all CHPs except AMV4, which is obtained from [Varmeplan Hovedstaden](https://varmeplanhovedstaden.dk/).

C~b~ is calculated as follows: 
$$
    C_b = \frac{\eta_{electric}}{\eta_{total} -\eta_{electric}}
$$

Boiler ramping rates are taken from [Ommen et al, 2016](http://dx.doi.org/10.1016/j.energy.2015.10.063), and assumed 25% for AMV4.

The following spreadsheets from [Technology Catalogue - Generation](https://ens.dk/en/our-services/projections-and-models/technology-data/technology-data-generation-electricity-and) are used for costs:
- AMV1  : 09b Wood Pellets, Medium
- AMV4  : 09a Wood Chips, Large 50 degree
- HCV8  : 01 Coal CHP (*assumed, actually the system is a steam turbine*)
- HCV8  : 05 Gas turb. CC, Back-pressure
- KKV7  : 09a Wood Chips, Medium
- KKV8  : 09a Wood Chips, Medium
- ARC   : 08 WtE CHP, Large, 50 degree
- ARGO5 : 08 WtE CHP, Medium
- ARGO6 : 08 WtE CHP, Medium
- VF5   : 08 WtE CHP, Medium
- VF6   : 08 WtE CHP, Medium

#### Extraction units

Total and electric efficiencies are obtained from [Ommen et al, 2016](http://dx.doi.org/10.1016/j.energy.2015.10.063).

C~v~ factors are obtained from [Ommen et al, 2014](http://dx.doi.org/10.1016/j.energy.2014.04.023).

C~b~factors are calculated as follows:
$$
    C_b = \frac{Y_{electric}}{Y_{heat}} - C_v
$$

Boiler ramping rates are taken from [Ommen et al, 2016](http://dx.doi.org/10.1016/j.energy.2015.10.063).

The following spreadsheets from [Technology Catalogue - Generation](https://ens.dk/en/our-services/projections-and-models/technology-data/technology-data-generation-electricity-and) are used for costs:
- AMV3  : 01 Coal CHP
- AVV1  : 09b Wood Pellets extract. plant
- AVV2  : 09b Wood Pellets extract. plant
# Generator data preparation notes

This file describes the process taken for retrieving data from the original file, and how it ends up in the final dataset.
It also describes assumptions made, and which criteria are these based on.


## Data cleaning procedure

### General cleaning

1. Removed all rows whose DH network is not Copenhagen.
2. Removed all rows whose year is not 2020.
3. Removed all rows without heat capacity.
4. Removed all rows whose "heat-delivered" share is 0%, i.e. heat is used solely for processes.
5. Removed all boilers whose main fuel is not indicated because of no production in 2020.


### Log of specific adjustments

- Geothermal heating plant (14 MW~h~ capacity) has been removed due to being a demonstration project and not having produced in 2020.

- Solar thermal unit has been removed due to low capacity (2.1 MW~h~) and capacity factor (8%) and extra complexity on including solar irradiance.

- The following CHPs have been removed due to low capacity:
  | Generator name              | Capacity (MW~h~)| Capacity factor (-) |
  |-----------------------------|-----------------|---------------------|
  | Damhusåen Renseanlæg        | 0.8             | 89%                 |
  | VEKS - Solrød Kedelcentral  | 3.7             | 85%                 |

 
- Direct excess-heat generators has been lumped together:
  | Generator name        | Capacity (MW~h~) | Capacity factor (-) |
  | --------------------- | ---------------- | --------------------|
  | CP Kelco ApS          | 7.0              | 77%                 |
  | Novo Nordisk          | 0.9              | 22%                 |
  | Ballerup Krematorium  | 0.2              | 33%                 |

- The following heat pumps have been consolidated, and simplified assuming air as energy source:
  | Generator name                    | Energy source        | Heat capacity (MW~h~) | Capacity factor (-) |
  |-----------------------------------|----------------------|-----------------------|---------------------|
  | Mølleholmen-centralen             | ground water         | 1.40                  | 47%                 |
  | Penta-Infra Datacenter Glostrup   | indirect excess-heat | 0.18                  | 85%                 |
  | Sjællandsbroens Pumpestation      | other                | 5.12                  | 9%                  |
  | UNICEF Supply Division            | ground water         | 1.00                  | 19%                 |
  | Novozymes                         | indirect excess-heat | 3.90                  | 7%                  |
  | Energivejcentralen                | other                | 1.00                  | 1%                  |
  | Helgeshøj Alle                    | indirect excess-heat | 1.40                  | 11%                 |
  | Litauen Alle                      | air                  | 3.20                  | 23%                 |
  | Varmepumpe Bjergmarken Renseanlæg | waste water          | 8.00                  | 13%                 |



- Svanemølleværket, is currently operated only as peaking heat plant according to [Ørsted](https://orsted.dk/vores-groenne-loesninger/bioenergi/vores-kraftvarmevaerker):
  - Blocks 1 and 7 (CHP units) have been removed because they are no longer in operation, at least from 2020, according to the Energy Producer Census 2022.
  - Boilers 21 and 22 are included as boiler units running on natural gas (HOB_NG).


## Commissioning and decommissioning

Some units have been decommissioned or commissioned in 2020, as stated in EPC 2022. The availability of these units is represented by the 'availability' factor in the model. The relevant units are shown below:

| Unit ID | Model name | Type             | Commissioning date | Decommissioning date | Fuel capacity |
| ------- | ---------- | ---------------- | ------------------ | -------------------- | ------------- |
| 2398-1  | HP         | HP - excess heat | 2020-07-01         |                      | 0.90          |
| 2407-1  | HP         | HP - waste water | 2020-09-01         |                      | 2.50          |
| 2402-1  | HP         | HP - excess heat | 2020-10-01         |                      | 0.35          |
| 1351-2  | HOB_EL     | boiler           | 2020-10-01         |                      | 80            |
| 330-3   | AMV3       | CHP              |                    | 2020-03-01           | 595           |

## CHP configuration

### Turbine configuration

Heating capacities stated in the Energy Producer Census (EPC) seem to not include turbine bypass. The following reasons apply:
- [ARC website](https://a-r-c.dk/amager-bakke/teknik/) mentions the existence of a turbine-bypass, while indicating a maximum heating capacity up to 247 MW~h~, which is in the range (although higher) of its boiler capacity.
- [HOFOR website](https://www.hofor.dk/baeredygtige-byer/fremtidens-fjernvarme/amagervaerket/blok-4-paa-amagervaerket/tekniske-facts-blok4/) also mentions the existence of a turbine-bypass for AMV4. It also clearly states nominal heating capacity that matches EPC, and explicitly states 150 MW~h~ extra due to turbine bypass.
- [Varmeplan Hovedstaden](https://varmeplanhovedstaden.dk/) technical data includes heating capacity and extra bypass capacity separately. Although they don't exactly match EPC, nominal capacities are in the range of what's stated in EPC.

- HCV 7: Its firing capacity is 200 MW, even though its heating capacity is significantly larger. The real boiler capacity is 285 MW, but it is restricted in its operation ([source](https://dma.mst.dk/vis-sag/1352675)). Additionally, EPC seems to indicate a heating capacity that includes bypass.

In a similar way, data from Varmeplan Hovedstaden seems to indicate that EPC reports condensing capacity.
* NOTES:

* S0: No excess heat recovery (imposed by fixing x_hr to zero)
* S1: Excess heat recovery at marginal-cost-pricing

* ======================================================================
*  Options
* ======================================================================
* option limrow = 100
* option limcol = 100
option optcr = 0.0001
option reslim = 1E6
$onEmpty

* ======================================================================
*  Load gdx data
* ======================================================================
* Setting defaults for local run
$setglobal timesteps        selected_weeks
$setglobal case             C2
$setglobal scenario         S1
$setglobal path_output      ../../results/%timesteps%/%case%/%timesteps%_%case%_%scenario%.gdx

* ======================================================================
*  Global scalars
* ======================================================================
SCALAR
$ifi %case% == C1 M_case    'Case multiplier'           /1/
$ifi %case% == C2 M_case    'Case multiplier'           /50/
;

* ======================================================================
*  Set declaration and definition
* ======================================================================
SETS
T                                   'Timesteps'
TECH                                'All generators'
I(TECH)                             'Lower level generators'
J(TECH)                             'Upper level generators'
F                                   'Fuels'
DD                                  'Days'
WW                                  'Weeks'
MM                                  'Months'
SOS                                 'SOS1 set'
I_F(I,F)                            'Mapping: DC generator - fuel'
J_F(J,F)                            'Mapping: DH generator - fuel'
;

SET SOS
/S1*S2/
;

SET T
/
$include    '../../datasets/timeseries-%timesteps%/%timesteps%_ts-timesteps.csv'
/;

Set DD
/
$include    '../../datasets/timeseries-%timesteps%/%timesteps%_ts-days.csv'
/;

SET WW
/
$include    '../../datasets/timeseries-%timesteps%/%timesteps%_ts-weeks.csv'
/;

Set MM
/
$include    '../../datasets/timeseries-%timesteps%/%timesteps%_ts-months.csv'
/;

SET TECH
/
$include    '../../datasets/generator-names.csv'
/;

SET I(TECH)
/
$include    '../../datasets/dc-generator-names.csv'
/;

SET J(TECH)
/
$include    '../../datasets/dh-generator-names.csv'
/;

SET F
/
$include    '../../datasets/fuel-names.csv'
/;

SET I_F(I,F)
/
$onDelim
$include    '../../datasets/dc-generator-fuels.csv'
$offDelim
/;
SET J_F(J,F)
/
$onDelim
$include    '../../datasets/dh-generator-fuels.csv'
$offDelim
/;

* ======================================================================
*  Auxiliary data loading (required after definition of sets, but before subsets)
* ======================================================================
ACRONYMS CO 'Cold-only', HR 'Heat recovery';
ACRONYMS EX 'Extraction', BP 'Backpressure', HO 'Heat-only';
ACRONYMS timeVar 'time-variable data'

SET GnrtAttrs(*)                    'Auxiliary set to load generator data'
/
$onDelim
$include    '../../datasets/generator-attributes.csv'
$offDelim
/;

SET FuelAttrs(*)                    'Auxiliary set to load fuel data'
/
$onDelim
$include    '../../datasets/fuel-attributes.csv'
$offDelim
/;

TABLE DC_GNRT_DATA(I,GnrtAttrs)     'Container for DC generator data'
$onDelim
$include    '../../datasets/dc-generator-data.csv'
$offDelim
;

TABLE DH_GNRT_DATA(J,GnrtAttrs)     'Container for DH generator data'
$onDelim
$include    '../../datasets/dh-generator-data.csv'
$offDelim
;

TABLE FUEL_DATA(F,FuelAttrs)        'Container for fuel data'
$onDelim
$include    '../../datasets/fuel-data.csv'
$offDelim
;

* ======================================================================
*  Subset declaration and definition
* ======================================================================
SETS
T_DD_map(T,DD)                      'Timestep-day mapping'
T_WW_map(T,WW)                      'Timestep-week mapping'
T_MM_map(T,MM)                      'Timestep-month mapping'
;

SETS 
T_DD_map(T,DD)
/
$onDelim
$include    '../../datasets/timeseries-%timesteps%/%timesteps%_ts-TDD-mapping.csv'
$offDelim
/

T_WW_map(T,WW)
/
$onDelim
$include    '../../datasets/timeseries-%timesteps%/%timesteps%_ts-TWW-mapping.csv'
$offDelim
/

T_MM_map(T,MM)
/
$onDelim
$include    '../../datasets/timeseries-%timesteps%/%timesteps%_ts-TMM-mapping.csv'
$offDelim
/
;

SETS
J_BP(J)                             'CHP generators - backpressure'
J_EX(J)                             'CHP generators - extraction'
J_CHP(J)                            'CHP generators'
J_HO(J)                             'Heat-only generators'
I_HR(I)                             'Heat-recovery generators'
I_CO(I)                             'Cold-only generators'
F_EL(F)                             'Fuel - electricity'
;

* --- Subset definition ---
J_BP(J)     = YES$(DH_GNRT_DATA(J,'TYPE') EQ BP);
J_EX(J)     = YES$(DH_GNRT_DATA(J,'TYPE') EQ EX);
J_HO(J)     = YES$(DH_GNRT_DATA(J,'TYPE') EQ HO);
I_HR(I)     = YES$(DC_GNRT_DATA(I,'TYPE') EQ HR);
I_CO(I)     = YES$(DC_GNRT_DATA(I,'TYPE') EQ CO);
F_EL(F)     = YES$(sameas(F,'electricity'));

* ----- Subset operations -----
J_CHP(J)    = J_BP(J) + J_EX(J);           

* ======================================================================
*  PARAMETERS
* ======================================================================
* ----- Parameter declaration -----
PARAMETERS
* Cost parameters
C_h(J)                              'Cost of heat production (EUR/MWh)'
C_e(J)                              'Cost of electricity production (EUR/MWh)'
C_c(I)                              'Cost of cold production (EUR/MWh)'
C_hr(I)                             'Cost of heat recovery (EUR/MWh)'
C_f_j(T,J)                          'DH Generator fuel-based cost (EUR/MWh)'
C_f_i(T,I)                          'DC Generator fuel-based cost (EUR/MWh)'
C_t                                 'Cost of transport for heat-recovery (EUR/MWh)'

* Generator parameters
Y_f(J)                              'Fuel capacity (MWh) - DH' 
Y_c(I)                              'Cold capacity (MWh) - DC (CO)'
Y_h(I)                              'Heat capacity (MWh) - DC (HR)'
F_a_i(T,I)                          'DC generator availability factor (-)'
F_a_j(T,J)                          'DH generator availability factor (-)'
eta_i(T,I)                          'DC generator efficiency (-)'
eta_j(T,J)                          'DH generator efficiency (-)'
beta_b(J)                           'CHP Cb ratio (-)'
beta_v(J)                           'CHP Cv ratio (-)'
rho_hr(TECH)                           'Transportation loss factor for heat-recovery (-)'

* Demand parameters
D_h(T)                              'Heat demand (MWh)'
D_c(T)                              'Cold demand (MWh)'
Tp_air(T)                           'Temperature of air (°C)'

* Fuel parameters
pi_e(T)                             'Price of electricity (EUR/MWh)'
pi_f(T,F)                           'Price of fuel (EUR/MWh)'
pi_co2(F)                           'Price of carbon quota (EUR/kg)'
q_e(T)                              'Carbon content in electricity (kg/MWh)'
q_f(T,F)                            'Carbon content in fuel (kg/MWh)'
;

* ----- Parameter definition -----
* - One-dimensional parameters -
PARAMETERS
D_h(T)
/
$onDelim
$include    '../../datasets/timeseries-%timesteps%/%timesteps%_ts-demand-heat.csv'
$offDelim
/

D_c(T)
/
$onDelim
$include    '../../datasets/timeseries-%timesteps%/%timesteps%_ts-demand-cold.csv'
$offDelim
/

pi_e(T)
/
$onDelim
$include    '../../datasets/timeseries-%timesteps%/%timesteps%_ts-electricity-price.csv'
$offDelim
/

q_e(T)
/
$onDelim
$include    '../../datasets/timeseries-%timesteps%/%timesteps%_ts-electricity-carbon.csv'
$offDelim
/

Tp_air(T)
/
$onDelim
$include    '../../datasets/timeseries-%timesteps%/%timesteps%_ts-air-temperature.csv'
$offDelim
/
;


* - Multi-dimensional parameters -
TABLE F_a_i(T,I)
$onDelim
$include    '../../datasets/timeseries-%timesteps%/%timesteps%_ts-availability-DC.csv'
$offDelim
;

TABLE F_a_j(T,J)
$onDelim
$include    '../../datasets/timeseries-%timesteps%/%timesteps%_ts-availability-DH.csv'
$offDelim
;

TABLE eta_j(T,J)
$onDelim
$include    '../../datasets/timeseries-%timesteps%/%timesteps%_ts-efficiency-DH.csv'
$offDelim
;

TABLE eta_i(T,I)
$onDelim
$ifi %case% == C1   $include    '../../datasets/timeseries-%timesteps%/%timesteps%_ts-efficiency-DC-distribution.csv'
$ifi %case% == C2   $include    '../../datasets/timeseries-%timesteps%/%timesteps%_ts-efficiency-DC-transmission.csv'
$offDelim
;

* - Assigned parameters -
C_h(J)$(J_HO(J))                            = DH_GNRT_DATA(J,'VOM_h');
C_e(J)$(J_CHP(J))                           = DH_GNRT_DATA(J,'VOM_e');
C_c(I)$(I_CO(I))                            = DC_GNRT_DATA(I,'VOM_c');
C_hr(I)$(I_HR(I))                           = DC_GNRT_DATA(I,'VOM_h');

beta_b(J)$(J_CHP(J))                        = DH_GNRT_DATA(J,'Cb');
beta_v(J)$(J_EX(J))                         = DH_GNRT_DATA(J,'Cv');

q_f(T,F)                                    = FUEL_DATA(F,'carbon content')$(NOT F_EL(F))   + q_e(T)$(F_EL(F));
pi_f(T,F)                                   = FUEL_DATA(F,'fuel price')$(NOT F_EL(F))       + pi_e(T)$(F_EL(F));
pi_co2(F)                                   = FUEL_DATA(F,'carbon price');

Y_f(J)                                      = DH_GNRT_DATA(J,'capacity - fuel');
Y_c(I)                                      = DC_GNRT_DATA(I,'capacity - cold')*M_case;

* both a bit above the average annual heat capacity, for a fixed cooling cap
$ifi %case% == C1   Y_h(I)$(I_HR(I))        = 1.35*M_case; 
$ifi %case% == C2   Y_h(I)$(I_HR(I))        = 1.50*M_case;

$ifi %case% == C1   rho_hr(I)$(I_HR(I))     = 0.00;
$ifi %case% == C2   rho_hr(I)$(I_HR(I))     = 0.05;

$ifi %case% == C1   C_t                     = 0.0;
$ifi %case% == C2   C_t                     = 0.5;

* - Parameter operations -
D_c(T)                                      = D_c(T)*M_case;    
C_f_i(T,I)                                  = sum(F$I_F(I,F), pi_f(T,F) + q_f(T,F)*pi_co2(F) + FUEL_DATA(F,'taxes'));
C_f_j(T,J)                                  = sum(F$J_F(J,F), pi_f(T,F) + q_f(T,F)*pi_co2(F) + FUEL_DATA(F,'taxes'));


* ======================================================================
*  Variable declaration
* ======================================================================
Free Variables
obj                                 'Objective function (EUR)' 
;

Positive Variables
x_e(T,J)                            'Production of electricity (MWh)'
x_h(T,J)                            'Production of heat (MWh)'
x_c(T,I)                            'Production of cold (MWh)'
x_hr(T,I)                           'Production of recovered-heat (MWh)'
x_f_i(T,I)                          'Consumption of fuel - DC (MWh)'
x_f_j(T,J)                          'Consumption of fuel - DH (MWh)'
;

* ======================================================================
*  Variable attributes
* ======================================================================

$ifi %scenario% == S0 x_hr.fx(T,I) = 0;

* ======================================================================
* Equation declaration
* ======================================================================
Equations
eq_obj                              'Objective function'
eq_heat_balance(T)                  'Heat balance'
eq_production_max_upper(T,J)        'Maximum fuel consumption: upper-level generators'
eq_production_HO(T,J)               'Energy production: heat-only generators'
eq_production_EX(T,J)               'Energy production: extraction CHP'
eq_production_BP(T,J)               'Energy production: backpressure CHP'
eq_ratio_BP(T,J)                    'Ratio of heat to electricity production: backpressure CHP'
eq_ratio_EX(T,J)                    'Ratio of heat to electricity production: extraction CHP'

eq_cold_balance(T)                  'Cold balance'
eq_production_cold(T,I)             'Energy production: cold'
eq_production_HR(T,I)               'Energy production: heat-recovery'
eq_production_max_CO(T,I)           'Maximum energy production: cold-only generators'
eq_production_max_HR(T,I)           'Maximum energy production: heat-recovery generators'

;

* ======================================================================
* Equation definition
* ======================================================================
eq_obj..                                        obj     =e= + sum((T,J),            C_f_j(T,J)          *x_f_j(T,J))
                                                            + sum((T,J)$J_HO(J),    C_h(J)              *x_h(T,J)) 
                                                            + sum((T,J)$J_CHP(J),   C_e(J)              *x_e(T,J))
                                                            - sum((T,J)$J_CHP(J),   pi_e(T)             *x_e(T,J))
                                                            + sum((T,I),            C_f_i(T,I)          *x_f_i(T,I))
                                                            + sum((T,I)$I_CO(I),    C_c(I)              *x_c(T,I))
                                                            + sum((T,I)$I_HR(I),    C_hr(I)             *x_hr(T,I))
                                                            + sum((T,I)$I_HR(I),    C_t                 *x_hr(T,I))
;

*----- Upper-level constraints -----*
eq_heat_balance(T)..                            sum(J, x_h(T,J)) + sum(I$I_HR(I), (1-rho_hr(I))*x_hr(T,I))                      =e= D_h(T);
eq_production_max_upper(T,J)..                  x_f_j(T,J)                                                                      =l= F_a_j(T,J)*Y_f(J);
eq_production_HO(T,J)$J_HO(J)..                 x_h(T,J)                        - eta_j(T,J)*x_f_j(T,J)                         =e= 0;
eq_production_EX(T,J)$(J_EX(J))..               x_e(T,J) + beta_v(J)*x_h(T,J)   - eta_j(T,J)*x_f_j(T,J)                         =e= 0;
eq_production_BP(T,J)$(J_BP(J))..               x_e(T,J) +           x_h(T,J)   - eta_j(T,J)*x_f_j(T,J)                         =e= 0;
eq_ratio_BP(T,J)$J_BP(J)..                      beta_b(J)*x_h(T,J) - x_e(T,J)                                                   =e= 0;
eq_ratio_EX(T,J)$J_EX(J)..                      beta_b(J)*x_h(T,J) - x_e(T,J)                                                   =l= 0;

*----- Lower-level constraints -----*
*--- Equality constraints ---*
eq_cold_balance(T)..                            sum(I, x_c(T,I))                                                                =e= D_c(T);
eq_production_cold(T,I)..                       x_c(T,I)    - eta_i(T,I)    *x_f_i(T,I)                                         =e= 0;
eq_production_HR(T,I)$I_HR(I)..                 x_hr(T,I)   - (eta_i(T,I)+1)*x_f_i(T,I)                                         =e= 0;
* eta_c + 1 = COP

*--- Inequality constraints ---*
eq_production_max_CO(T,I)$I_CO(I)..             x_c(T,I)                                                                        =l= F_a_i(T,I)*Y_c(I);
eq_production_max_HR(T,I)$I_HR(I)..             x_hr(T,I)                                                                       =l= F_a_i(T,I)*Y_h(I);

* ======================================================================
* Model definition
* ======================================================================
model
all_eqs                               'all equations'
/all/
;

all_eqs.optfile = 1;

* ======================================================================
* Solve statements
* ======================================================================
solve all_eqs using LP minimizing obj;

* ======================================================================
* Post-processing
* ======================================================================
* ----- Calculate net costs ----- *
PARAMETERS
OUT_OBJ
OUT_EHR_PRICE(T)
OUT_DH_FUEL_COST
OUT_DH_CHP_REVENUE
OUT_DH_VOM_COST
OUT_DH_EHR_TRANSPORT_COST
OUT_DH_EHR_PURCHASE_COST
OUT_DH_EHR_TOTAL_COST
OUT_DH_NET_COST
OUT_DC_FUEL_TOTAL_COST
OUT_DC_FUEL_EHR_COST
OUT_DC_VOM_TOTAL_COST
OUT_DC_VOM_EHR_COST
OUT_DC_EHR_REVENUE
OUT_DC_EHR_PROFIT
OUT_DC_NET_COST
;

OUT_OBJ                     = obj.l;
OUT_EHR_PRICE(T)            = SUM(I$I_HR(I),C_f_i(T,I)/(eta_i(T,I)+1) + C_hr(I));

OUT_DH_FUEL_COST            = sum((T,J), C_f_j(T,J) * x_f_j.l(T,J));
OUT_DH_CHP_REVENUE          = sum((T,J)$J_CHP(J), pi_e(T) * x_e.l(T,J));
OUT_DH_VOM_COST             = sum((T,J)$J_HO(J), C_h(J) * x_h.l(T,J)) + sum((T,J)$J_CHP(J), C_e(J) * x_e.l(T,J));
OUT_DH_EHR_TRANSPORT_COST   = sum((T,I)$I_HR(I),    C_t         * x_hr.l(T,I));
OUT_DH_EHR_PURCHASE_COST    = sum((T,I)$I_HR(I),    OUT_EHR_PRICE(T)  * x_hr.l(T,I));
OUT_DH_EHR_TOTAL_COST       = OUT_DH_EHR_PURCHASE_COST + OUT_DH_EHR_TRANSPORT_COST;
OUT_DH_NET_COST             = OUT_DH_FUEL_COST + OUT_DH_VOM_COST + OUT_DH_EHR_TOTAL_COST - OUT_DH_CHP_REVENUE;

OUT_DC_FUEL_TOTAL_COST      = sum((T,I), C_f_i(T,I) * x_f_i.l(T,I));
OUT_DC_FUEL_EHR_COST        = sum((T,I)$I_HR(I), C_f_i(T,I) * x_f_i.l(T,I));
OUT_DC_VOM_TOTAL_COST       = sum((T,I)$I_HR(I), C_hr(I) * x_hr.l(T,I)) + sum((T,I)$I_CO(I), C_c(I) * x_c.l(T,I));
OUT_DC_VOM_EHR_COST         = sum((T,I)$I_HR(I), C_hr(I) * x_hr.l(T,I));
OUT_DC_EHR_REVENUE          = sum((T,I)$I_HR(I), OUT_EHR_PRICE(T) * x_hr.l(T,I));;
OUT_DC_EHR_PROFIT           = OUT_DC_EHR_REVENUE - OUT_DC_VOM_EHR_COST - OUT_DC_FUEL_EHR_COST;
OUT_DC_NET_COST             = OUT_DC_FUEL_TOTAL_COST + OUT_DC_VOM_TOTAL_COST - OUT_DC_EHR_REVENUE;

* ----- Calculate generation (by type and fuel) ------ *
SET TYPE
/
$include    '../../datasets/tech-types.csv'
/;

SET TECH_TYPE(TECH,TYPE)
/
$onDelim
$include    '../../datasets/generator-tech-types.csv'
$offDelim
/;

SET TECH_FUEL(TECH,F)
/
#I_F, #J_F
/;

PARAMETERS
OUT_GENERATION_COLD(T,TECH,TYPE,F)      'Cold generation (MWh)'
OUT_GENERATION_HEAT(T,TECH,TYPE,F)      'Heat generation (MWh)'
OUT_GENERATION_ELEC(T,TECH,TYPE,F)      'Electricity generation (MWh)'
OUT_CONSUMPTION_FUEL(T,TECH,TYPE,F)     'Fuel consumption (MWh)'
OUT_CONSUMPTION_FUEL_TOTAL              'Total fuel consumption (MWh)'
;

OUT_GENERATION_COLD(T,TECH,TYPE,F)$(TECH_TYPE(TECH,TYPE) and TECH_FUEL(TECH,F))     = sum(I$(sameAs(TECH,I)),x_c.l(T,I));
OUT_GENERATION_HEAT(T,TECH,TYPE,F)$(TECH_TYPE(TECH,TYPE) and TECH_FUEL(TECH,F))     = sum(J$(sameAs(TECH,J)),x_h.l(T,J)) + sum(I$(sameAs(TECH,I)),x_hr.l(T,I));
OUT_GENERATION_ELEC(T,TECH,TYPE,F)$(TECH_TYPE(TECH,TYPE) and TECH_FUEL(TECH,F))     = sum(J$(sameAs(TECH,J)),x_e.l(T,J));
OUT_CONSUMPTION_FUEL(T,TECH,TYPE,F)$(TECH_TYPE(TECH,TYPE) and TECH_FUEL(TECH,F))    = sum(I$(sameAs(TECH,I)),x_f_i.l(T,I)) + sum(J$(sameAs(TECH,J)),x_f_j.l(T,J));
OUT_CONSUMPTION_FUEL_TOTAL                                                          = sum((T,TECH,TYPE,F), OUT_CONSUMPTION_FUEL(T,TECH,TYPE,F));

* ----- Calculate carbon emissions ------ *
PARAMETERS
OUT_CARBON_EMISSIONS(T,TECH,TYPE,F)
OUT_CARBON_EMISSIONS_DC_TOTAL
OUT_CARBON_EMISSIONS_DH_TOTAL
;

OUT_CARBON_EMISSIONS(T,TECH,TYPE,F) = q_f(T,F) * OUT_CONSUMPTION_FUEL(T,TECH,TYPE,F);
OUT_CARBON_EMISSIONS_DC_TOTAL       = sum((T,I,TYPE,F), OUT_CARBON_EMISSIONS(T,I,TYPE,F));
OUT_CARBON_EMISSIONS_DH_TOTAL       = sum((T,J,TYPE,F), OUT_CARBON_EMISSIONS(T,J,TYPE,F));


* ----- Calculate other indicators ------ *
PARAMETERS
OUT_SHARE_COLD(TECH,TYPE,F)
OUT_SHARE_HEAT(TECH,TYPE,F)
OUT_SHARE_FUEL(TECH,TYPE,F)
;

OUT_SHARE_COLD(TECH,TYPE,F) = sum(T, OUT_GENERATION_COLD(T,TECH,TYPE,F)) / sum(T, D_c(T));
OUT_SHARE_HEAT(TECH,TYPE,F) = sum(T, OUT_GENERATION_HEAT(T,TECH,TYPE,F)*(1-rho_hr(TECH)$(sameAs(TYPE,'HR')))) / sum(T, D_h(T));
OUT_SHARE_FUEL(TECH,TYPE,F) = sum(T, OUT_CONSUMPTION_FUEL(T,TECH,TYPE,F)) / OUT_CONSUMPTION_FUEL_TOTAL;


* ======================================================================
* Display
* ======================================================================
display "Timesteps, case and scenario:"
display '%timesteps%, %case%, %scenario%'

display "Variable levels"
display obj.l;
display OUT_EHR_PRICE;

* ======================================================================
* Output
* ======================================================================
execute 'mkdir ..\..\results\%timesteps%\%case%\';
execute_unload '%path_output%'

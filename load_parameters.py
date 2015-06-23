'''
Creator: Bryan Mayer
Created: 2/15/2015

This file contains parameters that varied across model runs and
 are friendly to user adjustment.

'''
#Length of Simulation
ND = 500 #years

#### contact rate (R0 ~= c / 10) ####
c = 160.

#### waning parameters ###
roBetaRate = 0.07 #log(2)/roBetaRate is the years to reach 50% susceptibility
prop = 4 #ratio of susceptibility to waning to contagiousness/duration, fixed to 4 in manuscript

#### OPV parameters ####
#relative contagiousness OPV:WPV
epsilon=np.sqrt(0.05)
#relative recovery rate OPV:WPV, this relationship is fixed
kappa = 1. / epsilon

##Vaccination Variables
vaccinate = True #vaccination program indicator, False=off

vaccRate = 1. #per year

vaccine_start_yr = 50  #year when vaccination starts, must be >= to 1 to work

vaccine_ramp_yrs = 2 #years it takes to reach vaccination rate (linear increase)




#these parameters are derived from other settings
### AVOID CHANGING THESE ###
TS = 0.1
t_start = 0.0; t_end = 0.5; t_inc = TS
t_range = np.arange(t_start, t_end, t_inc)
runEnd = np.size(t_range) - 1

vaccine_target_yr = vaccine_start_yr + vaccine_ramp_yrs #end of ramp up


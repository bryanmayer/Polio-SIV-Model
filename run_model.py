'''
Creator: Bryan Mayer
This is a re-creation of the original code: 2/15/2015
Results published in http://www.ncbi.nlm.nih.gov/pubmed/23592542

This main file sets up the model object
calls the simulation
automatically makes some plots
'''

import numpy as np
import scipy.integrate as spi
import pylab as pl
import time
import sys

#to import model object from the Code directory
sys.path.insert(0, 'Code/')
from polio_model_class import polio_model_class

storeOut = 0

#Parameter file -- change parameters in here
execfile('load_parameters.py')

#things that probably shouldn't be changed without care
execfile('Code/load_demographic.py')
execfile('Code/load_waning.py')
execfile('Code/polio_model.py')

#load initial values
INPUTload = np.loadtxt(open("Code/Input_data/example_initial.txt","r"))

#initialize model object
model = polio_model_class(n = n, m = m, dataIn = INPUTload)
model.staticParms(c, roBetaRate, epsilon, kappa, ND, theta)
model.vaccParms(vaccinate, vaccine_start_yr, vaccine_ramp_yrs)
avgAgePreVacc = model.avgAge()


##################  This is the where the model is simulated ####################
#for performance
start = time.time()

k = 0 #simulation index

while k <= ND / t_end:
    REStemp = spi.odeint(diff_eqs, model.INPUT, t_range)
    ### age() function stores the results, ages compartments by pulse and updates INPUT ###
    model.age(REStemp = REStemp, k = k, t_end = t_end, t_range = t_range)
    k += 1

end = time.time()

print end - start

#################################################################################


##################  Storing and graphing output #################################
avgAgePostVacc = model.avgAge()

# this stores the end of the results as the initial value for future simulations
# this is useful if you want to have the source population at steady state before introducing migration,
if storeOut == 1:
    np.savetxt("Code/Input_data/new_initial_values.txt", model.INPUT)


#this needs works #
iRES = model.RES[:, n * m:2 * n * m]
itotal = np.sum(iRES, axis = 1)
pop_total =np.sum(model.RES, axis = 1)
lastTime = 10 * ND + 4



t_rangePlot = np.arange(t_start, ND + .5, t_inc)

figprops = dict(figsize=(8., 8. / 1.618), dpi=128)
adjustprops = dict(left=0.1, bottom=0.1, right=0.97, top=0.93, wspace=0.2, hspace = 0.2)


#model.results(lastTime)
fig1 = pl.figure(**figprops)
fig1.subplots_adjust(**adjustprops)
ax = fig1.add_subplot(1, 1, 1)
ax.plot(t_rangePlot, itotal, label = 'Prev')
pl.xlabel('time (yr)')
pl.ylabel('prevalence')
pl.savefig('Output_figures/Prev.pdf')

#this is a sanity check for total population
#fig2 = pl.figure(**figprops)
#fig2.subplots_adjust(**adjustprops)
#ax2 = fig2.add_subplot(1, 1, 1)
#ax2.plot(t_rangePlot, pop_total, label = 'totalPop')
#pl.xlabel('time (yr)')
#pl.ylabel('population')
#pl.savefig('Output_figures/totalPop.pdf')







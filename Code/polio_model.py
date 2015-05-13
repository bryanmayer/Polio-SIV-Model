#model
def diff_eqs(INP,t):  
    '''The main set of equations'''

    #reorganize arrays
    inputState = polio_model_class(n, m, INP)
    diffEQ = polio_model_class(n, m)

    ######## MIGRATION ########
    dS = np.zeros((n, m))
    dI = np.zeros((n, m))
    dV = np.zeros((n, m))
  
    ######## Force of Infection WPV and OPV ########
    lambdaI = c * np.sum(theta * np.sum(inputState.I, axis = 1))
    lambdaV = (epsilon * c) * np.sum(theta * np.sum(inputState.V, axis = 1))

    ######## VACCINATION ########

    dSRecovered = np.zeros((n ,m))

    vaccOut = np.zeros((m, m))
    #vaccination program, only runs if vaccinaion=1, otherwise phi=0
    vaccTimeOn = ((k * 0.5) >= vaccine_start_yr)
    if vaccinate and vaccTimeOn:
        #if any vaccination on, and time > earliest implementation date
        phi = np.zeros((m))
        if (k * 0.5) < vaccine_target_yr:
			phi[0:ageGroupVacc] = ( ((k * 0.5) - vaccine_start_yr) / (vaccine_target_yr - vaccine_start_yr) ) * vaccRate
        else:
            phi[0:ageGroupVacc] = vaccRate
        
        vaccOut = np.diag(phi)

    ######## INFECTION DYNAMICS ########
    #this code utilizes matrix multiplication for ODEs

    #flows dependent on current state, Sij
    susceptibleS = np.dot(susceptibleOut, inputState.S)

    #force of infection varies by population (not by age or waning here)##
    dSInfI = lambdaI * susceptibleS
    dSInfV = lambdaV * susceptibleS

    #vaccination varies by both age and population
    dSVaccOut = np.dot(susceptibleS, vaccOut)

    #recovery processes independent of population#
    dIRecover = np.dot(durationOut, inputState.I)
    dVRecover = np.dot(kappa * durationOut, inputState.V)
    

    #epsilon = 0 means instant recovery from OPV (mimic IPV)
    if epsilon == 0:
        dSRecovered[n-1,] = np.sum(dIRecover, axis = 0) + np.sum(dSVaccOut,axis = 0)
    else:    
        dSRecovered[n-1,] = np.sum(dIRecover, axis = 0) + np.sum(dVRecover,axis = 0)


    ######## VITAL/WANING DYNAMICS ########
    #flows dependent on current state, Sij, does not vary by population/wane
    dSWaneOut = np.dot(waneOut, inputState.S)

    dSDeathOut = np.dot(inputState.S, deathOut)
    dIDeathOut = np.dot(inputState.I, deathOut)
    dVDeathOut = np.dot(inputState.V, deathOut)


    #flows dependent on other state e.g., Si-1,j
    #just shift outflows
    dSAge = np.zeros((n,m))
    dSAge[0, 0] = b
    dSWaneIn = np.vstack((dSWaneOut[1:n,], np.zeros((1,m))))
    
    diffEQ.S = dSAge + dSWaneIn + dSRecovered - dSWaneOut - (dSInfI + dSInfV + dSVaccOut) - dSDeathOut
    diffEQ.I = dSInfI - dIRecover - dIDeathOut

    #instant recovery from OPV (mimic IPV)
    if epsilon == 0:
        diffEQ.V = np.zeros((n, m))
    else:    
        diffEQ.V = (dSInfV + dSVaccOut) - dVRecover - dVDeathOut

    return diffEQ.makevector()   # For odeint

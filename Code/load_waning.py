n = 10  #wane states

####monophasic 3 parameters (actually 2 since rogamma=rotheta), roBetaRate varies
prop = 4 #ratio of suspectiblity waning: contagiousness or duration waning


roGammaRate = roBetaRate/prop
roThetaRate = roBetaRate/prop

#recovery rate bounds for WPV
gammaMin = 10.
gammaMax = 40.

#initializing parameters, gamma=duration,beta=susceptibility,theta=contagiousness 
gamma = np.zeros(n)
theta = np.zeros(n)
beta = np.zeros(n)
gamma[0] = gammaMin
beta[0] = theta[0] = 1

#waning rate vector, n = 10 waning stages
omegaInv = np.zeros(n)

#old set up with fast and slow parts to accent all of curve
FastImmStageDur = .5
SlowImmStageDur = 5.
numStageFast = 3.
numStageSlow = 5.
omegaInv[2:2+numStageSlow] = SlowImmStageDur
omegaInv[2+numStageSlow:n] = FastImmStageDur


#time-dependent function to define beta, gamma, and theta dynamics
def assignRo(t):

    roBeta = np.exp(-roBetaRate * t)
    roGamma = np.exp(-roGammaRate * t)
    roTheta = np.exp(-roThetaRate * t)  

    return [roBeta,roGamma,roTheta]

#parameter matrices
deathOut = np.zeros((m, m))
vaccOut = np.zeros((m, m))
susceptibleOut = np.zeros((n, n))
dSRecovered = np.zeros((n, m))
waneOut = np.zeros((n, n))
durationOut = np.zeros((n, n))


#and set up waning rates
#expect arrival time for each wane state, from simulation or could be analytical
for i in range(n):
    if i > 0:
        if i < n - 1:
            inputT = np.sum(omegaInv[i + 1:n])
        else:
            inputT = 0
        [roBeta,roGamma,roTheta] = assignRo(inputT)
        beta[i] = 1 - roBeta
        gamma[i] = gammaMin + roGamma * (gammaMax - gammaMin)
        theta[i] = 1 - roTheta
    susceptibleOut[i, i] = beta[i]
    durationOut[i, i] = gamma[i]
    if i>1:
        waneOut[i, i] = 1 / omegaInv[i]
    

for j in range(m):
    deathOut[j, j] = mu[j]
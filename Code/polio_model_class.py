import numpy as np

#these two functions are necessary for reshaping arrays to use odeint

#restructure returns 3-d array
def restructure(vector, n, m):
    return np.reshape(vector,(3,n,m))

#takes a 2-d array and turns it into stacked vector
def makepopvector(array, n, m):
    return np.reshape(array, n * m)

#n = immunity waning compartments
#m = age compartments
class polio_model_class():
    
    
    def __init__(self, n, m, dataIn = None, vaccTrans = True):

        self.n = n
        self.m = m

        #These are current state values##
        self.S = []
        self.I = []
        self.V = []

        self.N = []

        self.vaccLevel = []
        self.vaccLevelT = []
        self.vaccinate = 0.0


        #these are for model results#
        self.time = []
        self.susceptible = []
        self.infected = []
        self.vaccinated = []
        self.totalpop = []
        self.minPrev = 0.0
        self.minPrev75 = 0.0
        self.lambdaIout = 0.0
        self.lambdaIoutReinf = 0.0
        
        self.vaccTrans = vaccTrans

        if dataIn != None:
            self.INPUT = dataIn
            polio_model_class.loaddata(self)
        else:
            self.S = np.zeros((n, m))
            self.I = np.zeros((n, m))
            self.V = np.zeros((n, m))
            self.N = np.sum(self.S + self.I + self.V)
        self.INPUT = polio_model_class.makevector(self)

        polio_model_class.__ageParms__(self)

    def vaccParms(self, vaccinate, vaccine_start_yr, vaccine_ramp_yrs):
        self.vaccinate = vaccinate
        self.vaccine_start_yr = vaccine_start_yr
        self.vaccine_ramp_yrs = vaccine_ramp_yrs

    def staticParms(self, c, roBetaRate, epsilon, kappa, ND, theta):
        self.c = c
        self.roBetaRate = roBetaRate
        self.epsilon = epsilon
        self.kappa = kappa
        self.ND = ND
        self.theta = theta
         
    def loaddata(self):
        reshapedINPUT = restructure(self.INPUT, self.n, self.m)
        self.S = reshapedINPUT[0, :,]
        self.I = reshapedINPUT[1, :,]
        self.V = reshapedINPUT[2, :,]
        self.N = np.sum(reshapedINPUT)

    #this function stacks the population object into a vector for input into ODE algorithm
    def makevector(self):
        return np.hstack((makepopvector(self.S,self.n,self.m),makepopvector(self.I,self.n,self.m),makepopvector(self.V,self.n,self.m)))        
	
	#create results post-hoc
    def update(self, REStemp):

###this needs fixing!
            #update current state #
            REStempV = restructure(REStemp[i], self.n, self.m)
            self.susceptible = REStempV[0, :,]
            self.infected = REStempV[1, :,]
            self.vaccinated = REStempV[2, :,]
            self.N = np.sum(REStempV)

            #make time list
            self.time.append(REStemp)
            #store results by compartments
            self.susceptible.append(self.S)
            self.infected.append(self.I)
            self.vaccinated.append(self.V)
            self.totalpop.append(self.N)
        
    
    def age(self, k, REStemp, t_end=0.5, t_range=np.arange(0, 0.5, 0.1)):
        '''
        Aging procedure called from Main allows pulse aging every time its called
        k is model iterator (k/t_end + t_range[i] = current time)
        '''
        if k == 0:
            self.RES = REStemp
        else:
            self.RES = np.vstack((self.RES, REStemp))

		
        REStemp_arr = restructure(REStemp[len(t_range) - 1], self.n, self.m)
        sREStemp = REStemp_arr[0, :,]
        iREStemp = REStemp_arr[1, :,]
        vREStemp = REStemp_arr[2, :,]
        polio_model_class.__age__(self, sREStemp, iREStemp, vREStemp)
                        

    def __age__(self, sREStemp, iREStemp, vREStemp, i=0):
        '''
        The pulse aging process
        '''
                
        ages0t5 = self.ageParms['0t5']
        ages5t15 = self.ageParms['5t15']
        m = self.ageParms['m']
        
        sREStempNew = np.zeros((self.n, self.m))
        iREStempNew = np.zeros((self.n, self.m))
        vREStempNew = np.zeros((self.n, self.m))

        #age0t5 ages every run
        sREStempNew[:, 1:(ages0t5)] = sREStemp[:, 0:(ages0t5 - 1)]
        iREStempNew[:, 1:(ages0t5)] = iREStemp[:, 0:(ages0t5 - 1)]
        vREStempNew[:, 1:(ages0t5)] = vREStemp[:, 0:(ages0t5 - 1)]

        #border ages0t5 to 5t15, age in every 0.5 years, but only age out once every year
        sREStempNew[:,(ages0t5)]=sREStemp[:,(ages0t5-1)]+sREStemp[:,(ages0t5)]/2
        iREStempNew[:,(ages0t5)]=iREStemp[:,(ages0t5-1)]+iREStemp[:,(ages0t5)]/2
        vREStempNew[:,(ages0t5)]=vREStemp[:,(ages0t5-1)]+vREStemp[:,(ages0t5)]/2

        #age5t15, ages onces every year, half remains in, half moves out per 0.5 year run
        sREStempNew[:,(ages0t5+1):(ages5t15)]=sREStemp[:,(ages0t5):(ages5t15-1)]/2+sREStemp[:,(ages0t5+1):(ages5t15)]/2
        iREStempNew[:,(ages0t5+1):(ages5t15)]=iREStemp[:,(ages0t5):(ages5t15-1)]/2+iREStemp[:,(ages0t5+1):(ages5t15)]/2
        vREStempNew[:,(ages0t5+1):(ages5t15)]=vREStemp[:,(ages0t5):(ages5t15-1)]/2+vREStemp[:,(ages0t5+1):(ages5t15)]/2 


        #border age5t15 to 15p
        sREStempNew[:,(ages5t15)]=sREStemp[:,(ages5t15-1)]/2+sREStemp[:,(ages5t15)]*9/10
        iREStempNew[:,(ages5t15)]=iREStemp[:,(ages5t15-1)]/2+iREStemp[:,(ages5t15)]*9/10
        vREStempNew[:,(ages5t15)]=vREStemp[:,(ages5t15-1)]/2+vREStemp[:,(ages5t15)]*9/10

        #age15p, 1/10 moves out every 0.5 years, 9/10 stays in
        sREStempNew[:, (ages5t15 + 1):(m - 1)] = sREStemp[:, (ages5t15):(m - 2)]/10 + sREStemp[:, (ages5t15 + 1):(m - 1)] * 9/10
        iREStempNew[:, (ages5t15 + 1):(m - 1)] = iREStemp[:, (ages5t15):(m - 2)]/10 + iREStemp[:, (ages5t15 + 1):(m - 1)] * 9/10
        vREStempNew[:, (ages5t15 + 1):(m - 1)] = vREStemp[:, (ages5t15):(m - 2)]/10 + vREStemp[:, (ages5t15 + 1):(m - 1)] * 9/10

        #last compartment, age m, saturation
        sREStempNew[:, (m - 1)] = sREStemp[:, (m - 2)]/10 + sREStemp[:, (m - 1)]
        iREStempNew[:, (m - 1)] = iREStemp[:, (m - 2)]/10 + iREStemp[:, (m - 1)]
        vREStempNew[:, (m - 1)] = vREStemp[:, (m - 2)]/10 + vREStemp[:, (m - 1)]

        newSinit = makepopvector(sREStempNew, self.n, self.m)
        newIinit = makepopvector(iREStempNew, self.n, self.m)
        newVinit = makepopvector(vREStempNew, self.n, self.m)

        self.INPUT = np.hstack((newSinit, newIinit, newVinit))

    def results(self, lastTime):
        self.lastTime = lastTime     
        print np.shape(self.infected)
        self.inf = (np.sum(np.sum(self.infected, axis = 2), axis=1)) #by time
        self.totalpop = np.array(self.totalpop)
        X = self.totalpop.T    
        self.prev = self.inf/X
        polio_model_class.__min__(self)
        polio_model_class.__reinf__(self)

        self.plottime = np.arange(0, lastTime + 1, 1) / 10.

    def avgAge(self):
        #returns current average age, but also updates average age over time
        if np.shape(self.infected)[0] != 0:
             tempAge = np.array(self.infected)[0, 0, ]
             self.ageTime = np.sum(tempAge*self.ageAvg, axis=1)/np.sum(tempAge, axis=1)

        return np.sum((self.I[0]/np.sum(self.I[0]))*self.ageAvg)

    def plotter1D(self, plotvar, name = 'noname'):
        import pylab as pl
        figprops = dict(figsize=(8., 8. / 1.618), dpi=128)
        adjustprops = dict(left=0.1, bottom=0.1, right=0.97, top=0.93, wspace=0.2, hspace = 0.2)

        fig1 = pl.figure(**figprops)
        fig1.subplots_adjust(**adjustprops)
        ax = fig1.add_subplot(1, 1, 1)
        ax.plot(self.plottime,plotvar,label=name)
        pl.xlabel('time (yr)')
        pl.ylabel('prevalence')
        pl.legend()
        pl.savefig(name + '.pdf')

    def __ageParms__(self):
        self.ageParms = {}
        self.ageParms['vacc'] = 10
        self.ageParms['postvacc'] = 10
        self.ageParms['adult'] = 14
        self.ageParms['0t5'] = 10
        self.ageParms['5t15'] = 20
        self.ageParms['15p'] = 34
        self.ageParms['m'] = 34
        #below would need to be recoded if age changes from 34#
        self.ageAvg=np.zeros((self.ageParms['m']))
        self.ageAvg[0:10] = np.arange(0, 10) / 2.
        self.ageAvg[10:20] = np.arange(5, 15)
        self.ageAvg[20:34] = (np.arange(15, 85, 5) + np.arange(20, 90, 5)) / 2.

    def __min__(self):
        self.minPrev[:] = 0
        self.minPrev75[:] = 0

#Calculate the force of infection
    def __reinf__(self):
    	#overall
        self.lambdaIout[i] = np.sum(self.theta * np.sum(self.I, axis = 1))
        #ignore first infections for reinfection
        self.lambdaIoutReinf[i] = np.sum(self.theta[1:self.n] * np.sum(self.I[1:self.n, ],axis = 1))
       

if __name__ == '__main__':
    n = 10
    m = 34                         
    INPUTload = np.loadtxt(open("data/example_initial.txt","r"))
    testModel = polio_model_class(n=n, m=m, dataIn = INPUTload)
